#!/usr/bin/env bash
# wiki_build.sh — Launch ollama claude agent to build/update the wiki.
#
# Usage:
#   ./wiki_build.sh              # uses default model
#   ./wiki_build.sh glm-5:cloud  # override model
#
set -Eeuo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
WIKI_DIR="$REPO/wiki"
RAW_DIR="$WIKI_DIR/raw"
LLM_WIKI="$REPO/llm-wiki.md"
PROJECT_SCHEMA="$WIKI_DIR/WIKI.md"
MODEL="${1:-minimax-m2.7:cloud}"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

# ── Sanity checks ──────────────────────────────────────────────────────────
if [[ ! -d "$RAW_DIR" ]] || [[ -z "$(ls -A "$RAW_DIR" 2>/dev/null)" ]]; then
    log "wiki/raw/ is empty — nothing to build. Skipping."
    exit 0
fi

# ── Extract arxiv IDs from raw/ directory names ────────────────────────────
# Format: YYYY-MM-DD_arxiv_id or YYYY-MM-DD_XXXX.XXXXX
RAW_IDS=$(find "$RAW_DIR" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sed 's/.*_\([0-9]\{4\}\.[0-9]*\)$/\1/')

# ── Check for unprocessed papers ───────────────────────────────────────────
PROCESSED_FILE="$WIKI_DIR/processed.json"
PAPER_COUNT=0

if [[ -f "$PROCESSED_FILE" ]]; then
    # Count how many are new
    for id in $RAW_IDS; do
        if ! grep -q "\"$id\"" "$PROCESSED_FILE"; then
            ((PAPER_COUNT++))
        fi
    done

    if [[ "$PAPER_COUNT" -eq 0 ]]; then
        log "All papers in wiki/raw/ already processed — skipping build."
        exit 0
    fi
else
    # No processed.json yet, all papers are new
    PAPER_COUNT=$(echo "$RAW_IDS" | wc -w | tr -d ' ')
fi

if ! command -v ollama >/dev/null 2>&1; then
    echo "ERROR: ollama not found in PATH" >&2
    exit 1
fi

log "Building wiki for $PAPER_COUNT new paper(s) using model: $MODEL"

# ── Build the task prompt ──────────────────────────────────────────────────
TASK_PROMPT="$(cat <<PROMPT
You are maintaining a research paper wiki for the daily_paper project.

Below are two documents that define your task:

=== GENERAL WIKI PATTERN (llm-wiki.md) ===
$(cat "$LLM_WIKI")

=== PROJECT-SPECIFIC SCHEMA (WIKI.md) ===
$(cat "$PROJECT_SCHEMA")

=== YOUR TASK ===

Working directory: $REPO

There are $PAPER_COUNT new paper(s) staged in wiki/raw/ that have not yet been added to the wiki.

For each subdirectory in wiki/raw/:
1. Read summary.json and pdf.txt
2. Follow the ingest workflow defined in WIKI.md exactly
3. Create or update all necessary files in wiki/papers/, wiki/topics/, wiki/index.md, wiki/log.md
4. After all papers are processed, update wiki/processed.json

Be thorough with topic synthesis — the goal is a wiki where each topic page is a genuine cross-paper synthesis, not just a list of papers. Use the full PDF text (pdf.txt) to go beyond the AI summary.

Start now.
PROMPT
)"

# ── Launch the agent ───────────────────────────────────────────────────────
log "Launching ollama claude agent..."
cd "$REPO"

ollama launch claude \
    --model "$MODEL" \
    --yes \
    -- \
    -p "$TASK_PROMPT" \
    --dangerously-skip-permissions 2>&1 | tee -a "$REPO/wiki_build.log"

log "Wiki build complete."
