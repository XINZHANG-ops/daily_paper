#!/usr/bin/env bash
# wiki_rebuild.sh — Delete current wiki and rebuild from last 7 days with new schema.
#
# Usage:
#   bash wiki_rebuild.sh              # uses default model
#   bash wiki_rebuild.sh glm-5:cloud  # override model
#
set -Eeuo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
WIKI_DIR="$REPO/wiki"
MODEL="${1:-minimax-m2.7:cloud}"
REBUILD_START_DATE="2026-04-09"
ORIGINAL_START_DATE="2026-04-06"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

# ── Step 1: Delete current wiki content (keep pdf_cache) ─────────────────
log "Step 1: Cleaning wiki content (keeping pdf_cache/)..."
rm -rf "$WIKI_DIR/papers" "$WIKI_DIR/topics" "$WIKI_DIR/entities" "$WIKI_DIR/ideas"
rm -f "$WIKI_DIR/index.md" "$WIKI_DIR/log.md" "$WIKI_DIR/processed.json"
rm -rf "$WIKI_DIR/raw"

mkdir -p "$WIKI_DIR/papers" "$WIKI_DIR/topics" "$WIKI_DIR/entities" "$WIKI_DIR/ideas"

# Seed index.md
cat > "$WIKI_DIR/index.md" <<'EOF'
# Wiki Index

Last updated: — | Papers: 0 | Topics: 0 | Entities: 0 | Ideas: 0

## Papers

| arXiv ID | Title | Date Added | Topics |
|----------|-------|------------|--------|

## Topics

| Topic | Papers | Last Updated |
|-------|--------|-------------|

## Entities

| Entity | Type | Papers | Last Updated |
|--------|------|--------|-------------|

## Ideas

| Idea | Source | Last Updated |
|------|--------|-------------|
EOF

# Seed log.md
echo "# Wiki Log" > "$WIKI_DIR/log.md"

# Seed processed.json
echo '{"processed": []}' > "$WIKI_DIR/processed.json"

log "  Wiki cleaned. pdf_cache preserved."

# ── Step 2: Temporarily set START_DATE for rebuild ────────────────────────
log "Step 2: Setting START_DATE to $REBUILD_START_DATE for rebuild..."
sed -i.bak "s/^START_DATE = \".*\"/START_DATE = \"$REBUILD_START_DATE\"/" "$REPO/wiki_sync.py"

# ── Step 3: Run wiki_sync to stage papers + notes ────────────────────────
log "Step 3: Running wiki_sync.py..."
python -u "$REPO/wiki_sync.py"

# ── Step 4: Restore original START_DATE ───────────────────────────────────
log "Step 4: Restoring START_DATE to $ORIGINAL_START_DATE..."
sed -i.bak "s/^START_DATE = \".*\"/START_DATE = \"$ORIGINAL_START_DATE\"/" "$REPO/wiki_sync.py"
rm -f "$REPO/wiki_sync.py.bak"

# ── Step 5: Run wiki_build to create pages ────────────────────────────────
log "Step 5: Running wiki_build.sh with model: $MODEL..."
bash "$REPO/wiki_build.sh" "$MODEL"

# ── Step 6: Verify structure ──────────────────────────────────────────────
log "Step 6: Verifying wiki structure..."
echo "--- papers ---"
ls "$WIKI_DIR/papers/" 2>/dev/null || echo "(empty)"
echo "--- topics ---"
ls "$WIKI_DIR/topics/" 2>/dev/null || echo "(empty)"
echo "--- entities ---"
ls "$WIKI_DIR/entities/" 2>/dev/null || echo "(empty)"
echo "--- ideas ---"
ls "$WIKI_DIR/ideas/" 2>/dev/null || echo "(empty)"
echo "--- index.md header ---"
head -3 "$WIKI_DIR/index.md"

log "Wiki rebuild complete!"
