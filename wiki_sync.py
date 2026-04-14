#!/usr/bin/env python3
"""
wiki_sync.py — Prepare raw inputs for wiki building.

Steps:
  1. Load summaries.jsonl
  2. Download any PDFs missing from wiki/pdf_cache/
  3. Stage new (un-wikified) papers into wiki/raw/ for the agent to process
"""
import json
import re
import shutil
import time
from pathlib import Path

from loguru import logger
from utils.arxiv_utils import download_paper_text

# ── Paths ──────────────────────────────────────────────────────────────────
REPO_ROOT     = Path(__file__).parent
SUMMARIES     = REPO_ROOT / "summaries.jsonl"
WIKI_DIR      = REPO_ROOT / "wiki"
PDF_CACHE     = WIKI_DIR / "pdf_cache"
RAW_DIR       = WIKI_DIR / "raw"
PROCESSED     = WIKI_DIR / "processed.json"

# Only process papers added on or after this date (YYYY-MM-DD).
# Papers before this date are ignored for both PDF download and wiki building.
START_DATE = "2026-04-06"

# Seconds to wait between arxiv requests to avoid rate-limiting
DOWNLOAD_DELAY = 3


# ── Helpers ────────────────────────────────────────────────────────────────

def load_summaries() -> list[dict]:
    papers = []
    with open(SUMMARIES, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                papers.append(json.loads(line))
    return papers


def extract_arxiv_id(url: str) -> str | None:
    """Pull the arXiv numeric ID from a PDF URL."""
    m = re.search(r"arxiv\.org/(?:pdf|abs)/(\d+\.\d+)", url or "")
    return m.group(1) if m else None


def load_processed() -> set[str]:
    if PROCESSED.exists():
        data = json.loads(PROCESSED.read_text(encoding="utf-8"))
        return set(data.get("processed", []))
    return set()


def safe_dirname(s: str) -> str:
    """Strip characters unsafe for directory names."""
    return re.sub(r'[^\w\-]', '_', s)[:80]


def filter_papers(papers: list[dict]) -> list[dict]:
    """Return only papers whose date_added >= START_DATE."""
    result = []
    for paper in papers:
        date_str = paper.get("date") or paper.get("published_at") or ""
        date_str = date_str.strip()[:10]  # keep YYYY-MM-DD portion only
        if date_str >= START_DATE:
            result.append(paper)
    return result


# ── Step 1: download missing PDFs ──────────────────────────────────────────

def download_missing_pdfs(papers: list[dict]) -> dict[str, Path]:
    """
    Ensure every paper has its PDF text in pdf_cache/.
    Returns mapping arxiv_id -> cache_path for all successfully cached papers.
    """
    PDF_CACHE.mkdir(parents=True, exist_ok=True)
    cached: dict[str, Path] = {}
    missing = []

    for paper in papers:
        arxiv_id = extract_arxiv_id(paper.get("url", ""))
        if not arxiv_id:
            continue
        cache_path = PDF_CACHE / f"{arxiv_id}.txt"
        if cache_path.exists():
            cached[arxiv_id] = cache_path
        else:
            missing.append((arxiv_id, paper))

    logger.info(f"PDF cache: {len(cached)} cached, {len(missing)} to download")

    for i, (arxiv_id, paper) in enumerate(missing, 1):
        cache_path = PDF_CACHE / f"{arxiv_id}.txt"
        logger.info(f"[{i}/{len(missing)}] Downloading {arxiv_id} — {paper.get('title','')[:60]}")
        try:
            # arxiv_utils.download_paper_text expects 'paper_id' field
            paper_with_id = {**paper, 'paper_id': arxiv_id}
            result = download_paper_text(paper_with_id)
            if result["success"] and result["text"]:
                cache_path.write_text(result["text"], encoding="utf-8")
                cached[arxiv_id] = cache_path
                logger.info(f"  ✓ {result['pages']} pages saved")
            else:
                logger.warning(f"  ✗ Download failed: {result['message']}")
        except Exception as e:
            logger.error(f"  ✗ Exception: {e}")

        if i < len(missing):
            time.sleep(DOWNLOAD_DELAY)

    return cached


# ── Step 2: stage new papers into wiki/raw/ ────────────────────────────────

def stage_new_papers(papers: list[dict], cached_pdfs: dict[str, Path], processed: set[str]) -> int:
    """
    Copy summary + pdf text into wiki/raw/ for each paper not yet wikified.
    Returns count of papers staged.

    Note: raw/ is a permanent archive of all source materials, never cleared.
    Directories already in raw/ are skipped to avoid duplicates.
    """
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    staged = 0
    for paper in papers:
        arxiv_id = extract_arxiv_id(paper.get("url", ""))
        if not arxiv_id:
            continue
        if arxiv_id in processed:
            continue
        if arxiv_id not in cached_pdfs:
            logger.warning(f"No PDF cached for {arxiv_id}, skipping staging")
            continue

        date_str = paper.get("date", paper.get("published_at", "unknown"))
        dir_name  = f"{date_str}_{arxiv_id}"
        stage_dir = RAW_DIR / dir_name

        # Skip if already staged (raw/ is permanent)
        if stage_dir.exists():
            logger.info(f"  Already staged: {dir_name}, skipping")
            continue

        stage_dir.mkdir(parents=True, exist_ok=True)

        # Write summary.json (exclude the SVG flow_chart to save space)
        summary_data = {k: v for k, v in paper.items() if k != "flow_chart"}
        (stage_dir / "summary.json").write_text(
            json.dumps(summary_data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        # Symlink (or copy) the PDF text
        pdf_src  = cached_pdfs[arxiv_id]
        pdf_dest = stage_dir / "pdf.txt"
        shutil.copy2(pdf_src, pdf_dest)

        staged += 1
        logger.info(f"  Staged: {dir_name}")

    return staged


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    logger.info("=== wiki_sync.py starting ===")

    logger.info("Loading summaries.jsonl...")
    all_papers = load_summaries()
    papers = filter_papers(all_papers)
    logger.info(f"  {len(all_papers)} papers total, {len(papers)} on or after {START_DATE}")

    logger.info("Step 1: Downloading missing PDFs...")
    cached_pdfs = download_missing_pdfs(papers)
    logger.info(f"  {len(cached_pdfs)} PDFs available in cache")

    logger.info("Step 2: Staging new papers for wiki building...")
    processed = load_processed()
    logger.info(f"  {len(processed)} papers already wikified")
    staged = stage_new_papers(papers, cached_pdfs, processed)

    if staged == 0:
        logger.info("  No new papers to stage — wiki is up to date")
    else:
        logger.info(f"  {staged} papers staged in wiki/raw/")

    logger.info("=== wiki_sync.py done ===")
    return staged


if __name__ == "__main__":
    main()
