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
RAW_IDS=$(find "$RAW_DIR" -mindepth 1 -maxdepth 1 -type d -not -name '_all_notes' -exec basename {} \; | sed 's/.*_\([0-9]\{4\}\.[0-9]*\)$/\1/')

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

# ── Check for notes ───────────────────────────────────────────────────────
NOTES_DIR="$RAW_DIR/_all_notes"
NOTES_COUNT=0
if [[ -d "$NOTES_DIR" ]] && [[ -n "$(ls -A "$NOTES_DIR" 2>/dev/null)" ]]; then
    NOTES_COUNT=$(find "$NOTES_DIR" -name "*.md" -type f | wc -l | tr -d ' ')
fi
log "Found $NOTES_COUNT personal notes in _all_notes/"

# ── Check for chat sessions ───────────────────────────────────────────────
SESSIONS_DIR="$REPO/wiki_sessions"
SESSION_COUNT=0
if [[ -d "$SESSIONS_DIR" ]] && [[ -n "$(ls -A "$SESSIONS_DIR"/*.json 2>/dev/null)" ]]; then
    SESSION_COUNT=$(find "$SESSIONS_DIR" -name "*.json" -type f | wc -l | tr -d ' ')
fi
log "Found $SESSION_COUNT chat sessions in wiki_sessions/"

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
There are $NOTES_COUNT personal reading notes in wiki/raw/_all_notes/ to scan for ideas.
There are $SESSION_COUNT chat sessions in wiki_sessions/ with past Q&A conversations.

STEP 1 — Process each paper:
For each subdirectory in wiki/raw/ (SKIP _all_notes):
1. Read summary.json, pdf.txt, and notes.md (if present)
2. Follow the ingest workflow defined in WIKI.md exactly
3. Create/update files in wiki/papers/, wiki/topics/, wiki/entities/, wiki/ideas/
4. CRITICAL: Every ## Connections section must have ANNOTATED [[wikilinks]]. Read the Connection Rules in WIKI.md carefully. Never write "Related:" or "See also:" — always explain WHY.

STEP 2 — Process personal notes:
After all papers are processed, read notes from wiki/raw/_all_notes/:
1. Read each note file — these contain the reader's own insights about papers they read
2. Find connections between note insights and existing wiki content
3. Create wiki/ideas/ pages for cross-cutting insights found in notes
4. Add ## Personal Notes section to paper pages where the note date matches a paper date
5. Update entity and topic pages if notes mention relevant concepts

STEP 3 — Learn from chat history:
If wiki_sessions/ has JSON files, read them. Each file is a JSON array of {role, content} messages.
Look for:
- Questions the user asked that reveal knowledge gaps in the wiki → fill those gaps
- Insights or connections mentioned in Q&A that should be added to idea/topic/entity pages
- Repeated questions about the same topic → that topic page needs more depth
- Corrections or clarifications from conversations → update affected pages
Do NOT copy raw Q&A into the wiki. Extract the useful knowledge and integrate it naturally.

STEP 4 — Finalize:
1. Update wiki/index.md with all 4 sections (Papers, Topics, Entities, Ideas)
2. Update wiki/processed.json
3. Append to wiki/log.md

Be thorough with:
- Topic synthesis — each topic's ## Evolution should tell a chronological story, not list papers
- Entity identification — extract specific named models, datasets, algorithms from papers
- Idea extraction — find cross-cutting insights, especially from personal notes
- Connection quality — every [[wikilink]] must have a WHY annotation

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
    --permission-mode dontAsk 2>&1 | tee -a "$REPO/wiki_build.log"

log "Wiki build complete."
