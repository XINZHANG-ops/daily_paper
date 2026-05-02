#!/usr/bin/env bash
# wiki_lint.sh — Launch ollama claude agent to lint/self-reflect the wiki.
#
# Checks broken links, removes wrong/duplicate info, improves connections.
# Scheduled to run daily at 11 PM via launchd.
#
# Usage:
#   ./wiki_lint.sh              # uses default model
#   ./wiki_lint.sh glm-5:cloud  # override model
#
set -Eeuo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
WIKI_DIR="$REPO/wiki"
LLM_WIKI="$REPO/llm-wiki.md"
PROJECT_SCHEMA="$WIKI_DIR/WIKI.md"
MODEL="${1:-minimax-m2.7:cloud}"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

if [[ ! -d "$WIKI_DIR" ]]; then
    log "wiki/ directory not found — nothing to lint."
    exit 0
fi

if ! command -v ollama >/dev/null 2>&1; then
    echo "ERROR: ollama not found in PATH" >&2
    exit 1
fi

log "Starting wiki lint using model: $MODEL"

cd "$REPO"
git pull --ff-only || true

TASK_PROMPT="$(cat <<PROMPT
You are performing a daily self-reflection and health check on the daily_paper research wiki.

=== GENERAL WIKI PATTERN (llm-wiki.md) ===
$(cat "$LLM_WIKI")

=== PROJECT-SPECIFIC SCHEMA (WIKI.md) ===
$(cat "$PROJECT_SCHEMA")

=== YOUR TASK: WIKI LINT ===

Working directory: $REPO
Today's date: $(date '+%Y-%m-%d')

Perform a thorough lint of the wiki at wiki/. Go through EVERY check below systematically. Fix problems as you find them — don't just report, actually edit the files.

## Pass 1 — Structural Integrity

1. Read wiki/index.md. For every page listed, verify the .md file exists. Remove entries for missing files.
2. Scan wiki/papers/, wiki/topics/, wiki/entities/, wiki/ideas/ for .md files NOT listed in index.md. Add them.
3. Check all [[wikilinks]] across all pages. For each broken link (target doesn't exist):
   - If the target is a minor reference, remove the link
   - If the target is an important concept that should have a page, create it
4. Find orphan pages (no inbound links from any other page). Add links from relevant pages or note them for review.
5. Check topic pages: does paper_count match the actual number of papers in Key Papers table? Fix mismatches.
6. Check entity pages: do any have zero paper appearances? If so, add appearances from papers that mention them, or remove the entity if truly unused.
7. Check idea pages: do any have zero evidence links? Add evidence or remove if unsupported.

## Pass 2 — Wrong & Duplicate Information

1. Look for duplicate pages covering the same concept (e.g., two entity pages for the same model with slight name variations). Merge them — keep the richer one, redirect links.
2. Look for duplicate content within pages (same paragraph or section repeated).
3. Check for factually inconsistent information between pages (e.g., a paper's date differs between its paper page and a topic page).
4. Check frontmatter: are dates, slugs, and types consistent and correct?
5. Remove any people from entities/ — entities are for technical things only.

## Pass 3 — Connection Quality

1. Find connections that just say "Related:", "See also:", or link without annotation → rewrite with WHY.
2. Find papers that share 2+ entities but have no direct connection to each other → add annotated connections.
3. Check topic pages for missing ## Evolution section → write chronological narrative.
4. Check topic pages for missing ## Patterns & Insights → synthesize from papers.
5. Check for shallow entity pages with only a name and no description → flesh out from paper content.

## Pass 4 — Index & Log

1. Rebuild wiki/index.md with accurate counts and all pages listed.
2. Append a lint entry to wiki/log.md:
   ## [$(date '+%Y-%m-%d')] lint | self-reflection
   - Broken links fixed: N
   - Duplicates merged: N
   - Orphans resolved: N
   - Connections improved: N

Start now. Be thorough but efficient.
PROMPT
)"

ollama launch claude \
    --model "$MODEL" \
    --yes \
    -- \
    -p "$TASK_PROMPT" \
    --permission-mode dontAsk 2>&1 | tee -a "$REPO/logs/lint.log"

EXIT_CODE=$?
log "Wiki lint complete (exit code $EXIT_CODE)."

cd "$REPO"
git add -A
git commit -m "wiki: lint $(date '+%Y-%m-%d')" || true
git push || true

exit $EXIT_CODE
