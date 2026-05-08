import re
from pathlib import Path

wiki = Path("wiki")

print("=== Checking papers appear in their frontmatter topic tables ===")
for p in (wiki/"papers").glob("*.md"):
    text = p.read_text()
    fm = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not fm:
        continue
    content = fm.group(1)
    topics_match = re.search(r"topics:\s*\[(.*?)\]", content)
    if topics_match:
        topics = [t.strip().strip("'\"").strip() for t in topics_match.group(1).split(",")]
    else:
        topics_match = re.search(r"topics:\s*\n((?:\s+-\s+\S+\n)+)", content)
        if topics_match:
            topics = [t.strip().strip("- ").strip() for t in topics_match.group(1).strip().split("\n")]
        else:
            topics = []

    for topic in topics:
        tfile = wiki / "topics" / f"{topic}.md"
        if not tfile.exists():
            print("  " + p.name + " references missing topic: " + topic)
            continue
        ttext = tfile.read_text()
        if f"[[{p.stem}]]" not in ttext:
            print("  " + p.name + " missing from topic table: " + topic)

print("\n=== Checking topic paper_count vs Key Papers table (strict) ===")
for t in (wiki/"topics").glob("*.md"):
    text = t.read_text()
    fm = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    paper_count = None
    if fm:
        m = re.search(r"paper_count:\s*(\d+)", fm.group(1))
        if m:
            paper_count = int(m.group(1))

    m = re.search(r"## Key Papers\s*\n\|.*?\|\s*\n\|.*?\|\s*\n((?:\|.*?\|\s*\n)*)", text)
    actual = 0
    if m:
        rows = [r for r in m.group(1).strip().split("\n") if r.strip().startswith("|")]
        actual = len(rows)

    if paper_count is not None and paper_count != actual:
        print("  " + t.name + ": paper_count=" + str(paper_count) + " actual=" + str(actual))

print("\n=== Checking for empty Personal Notes ===")
for p in (wiki/"papers").glob("*.md"):
    text = p.read_text()
    if "## Personal Notes" in text:
        m = re.search(r"## Personal Notes\s*\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
        if m:
            content = m.group(1).strip()
            if not content or len(content) < 20:
                print("  Empty/short notes in " + p.name)

print("\n=== Checking for missing Evolution or Patterns sections ===")
for t in (wiki/"topics").glob("*.md"):
    text = t.read_text()
    if "## Evolution" not in text:
        print("  Missing ## Evolution: " + t.name)
    if "## Patterns & Insights" not in text:
        print("  Missing ## Patterns & Insights: " + t.name)
