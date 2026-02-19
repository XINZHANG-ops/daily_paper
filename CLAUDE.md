# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Daily Paper is an automated AI research paper tracking system that fetches papers from HuggingFace, generates AI summaries with quizzes and flowcharts, and publishes to GitHub Pages. The system supports vector search, SQL queries, and an integrated AI chat assistant.

**Live Site**: https://xinzhang-ops.github.io/daily_paper/

## Common Commands

### Daily Paper Processing
```bash
# Main workflow: fetch papers, generate summaries, post to Google Chat, update GitHub Pages
python daily_papers.py

# Start on main branch (script does git pull automatically)
git switch main && python daily_papers.py
```

### Vector Search Index
```bash
# Incremental update (default, resumes from last checkpoint)
python build_index.py --summaries summaries.jsonl

# Force rebuild from scratch
python build_index.py --summaries summaries.jsonl --force-rebuild --batch-size 3

# Change chunk parameters
python build_index.py --chunk-size 2500 --chunk-overlap 300 --embedding-model embeddinggemma:300m

# Rebuild FAISS index without re-generating embeddings
python rebuild_faiss.py --index-dir vector_indices/chunk2500_overlap300_model_embeddinggemma_300m --faiss-type HNSW
```

### Search API Server
```bash
# Start search API (default port 5001)
python serve_search.py \
  --index-dir vector_indices/chunk2500_overlap300_model_embeddinggemma_300m \
  --summaries-path summaries.jsonl \
  --sqlite-path papers.sqlite \
  --port 5001

# Rebuild SQLite database from summaries.jsonl
python serve_search.py --index-dir ... --overwrite-db
```

### AI Chat Backend
```bash
# Start AI assistant backend (default port 5000)
python flask_claude_server.py
```

### Testing Search
```bash
# Vector search
curl -X POST http://localhost:5001/search \
  -H "Content-Type: application/json" \
  -d '{"query": "transformer architecture", "k": 5}'

# SQL query
curl -X POST http://localhost:5001/query \
  -H "Content-Type: application/json" \
  -d '{"sql": "SELECT title, date_added FROM papers WHERE personal_notes IS NOT NULL"}'

# Get available metadata fields
curl http://localhost:5001/metadata_fields

# Get database schema
curl http://localhost:5001/schema
```

## Architecture

### Data Pipeline (daily_papers.py)

```
HuggingFace API
  ↓ get_huggingface_papers() [utils/huggingface_utils.py]
Filter (find_not_proposed_papers)
  ↓ process_paper() [utils/__init__.py] - 150s timeout per paper
  ├─ Download PDF [utils/arxiv_utils.py]
  ├─ Generate summary (5-point structure) [utils/ai_utils.py]
  ├─ Generate quiz (3 questions) [utils/ai_utils.py]
  └─ Generate flowchart (SVG) [utils/ai_utils.py]
  ↓
Append to summaries.jsonl
  ↓
Post to Google Chat [utils/google_chat_utils.py]
  ↓
Generate HTML pages [templates/]
  ├─ create_subpage() → dailies/pages/{date}.html
  └─ update_index_page() → index.html (year/month/day structure)
  ↓
Git commit + push
```

**Key details**:
- Processes max 3 papers per run (`paper_counts = 3`)
- Each paper has random background image from `bg/` folder
- Personal notes loaded from `dailies/notes/{date}.md` if exists (shows 📝 badge)
- Flowchart creates 2-card carousel, otherwise single card
- Uses `Threading` with `Queue` for timeout handling

### Vector Search Architecture

```
summaries.jsonl
  ↓ build_index.py
  ├─ create_chunks_from_paper()
  │  ├─ Chunk summary content (chunk_source='summary')
  │  └─ Download + chunk PDF (chunk_source='pdf_original')
  │     ↓ utils/arxiv_utils.download_paper_text()
  ↓
Embedding Generation (via Ollama)
  ↓ OllamaEmbeddings.embed_documents()
  ↓
Sharded Storage [search_engine_utils/embeddings_manager.py]
  ├─ embeddings/shard_0000.pkl (500 chunks each)
  ├─ embeddings/shard_0001.pkl
  └─ ...
  ↓
FAISS Index Creation
  ↓ FAISS.from_embeddings()
  ├─ index.faiss (vector index)
  └─ index.pkl (metadata)
```

**Key details**:
- Incremental updates tracked via `processed_papers.json`
- Saves every `batch_size` papers (default: 3) for auto-resume
- Two chunk sources per paper: AI summary + full PDF
- Personal notes added to metadata from `dailies/notes/{date_added}.md`
- `clean_text()` removes Unicode surrogate pairs and math symbols

### Search API Architecture (serve_search.py)

```
FAISS Index
  ↓ FAISS.load_local()
Documents
  ↓ Extract from docstore
HybridRetriever [search_engine_utils/hybrid_retriever.py]
  ├─ Vector Search (FAISS with config.vector_weight)
  └─ Keyword Search (BM25 with config.bm25_weight)
  ↓
Flask API
  ├─ POST /search - Hybrid vector+BM25 search
  ├─ POST /query - SQL queries (SELECT only)
  ├─ GET /metadata_fields - List available fields
  ├─ GET /schema - SQLite schema
  └─ GET /stats - Index statistics
```

**Key details**:
- SQLite built from summaries.jsonl on startup (unless exists)
- HybridRetriever combines vector + BM25 scores
- SQL injection protection: only SELECT, blocks dangerous keywords
- Port 5001 (default), binds to 0.0.0.0 for LAN access

### Frontend AI Assistant (js/ai-assistant-*.js)

**Modular Structure**:
- `ai-assistant-constants.js` - Constants (ICONS, CSS_CLASSES, CONTEXT_TYPES, etc.)
- `ai-assistant-storage.js` - StorageManager (localStorage wrapper)
- `ai-assistant-positioning.js` - PositionManager (chat window positioning)
- `ai-assistant-dom-utils.js` - DOMUtils (DOM helpers)
- `ai-assistant-templates.js` - Templates (HTML generators)
- `ai-assistant-config.js` - Server URL config (local vs ngrok)
- `ai-assistant.js` - Main AIAssistant class (1676 lines)

**Data Flow**:
```
User Input
  ↓ AIAssistant.sendMessage()
  ↓ POST /chat {message, session_id, current_page, context_type, paper_date}
flask_claude_server.py
  ↓ utils/models.model_response()
Claude API
  ↓ response
AIAssistant.addMessage('assistant', response)
  ↓ Templates.message() + renderMarkdown()
localStorage + DOM
```

**Key details**:
- Storage keys prefixed with `-paper` to avoid conflicts with personal_page repo
- Auto-detects `paper_date` from URL pathname `/pages/YYYY-MM-DD.html`
- Context type fixed to "paper" via `setDefaultContextTag()`
- Typing indicator bug fixed: removes entire message div via `.closest('.ai-message')`
- Draggable (toggle button only), resizable (dynamic corner handles)
- Markdown renderer in `renderMarkdown()` handles lists, bold, italic, links, code

### HTML Generation Architecture

**Templates** (`templates/` loaded via `utils/template_loader.py`):
- `index_template.html` - Main page with year/month/day collapsible structure
- `subpage_template.html` - Daily page with paper cards + quizzes

**Paper Cards**:
```html
<div class="paper-container">
  <div class="card-deck">  <!-- Only if flowchart exists -->
    <div class="card-counter">1/2</div>
    <div class="paper-card active">Summary</div>
    <div class="paper-card flowchart-card">SVG</div>
  </div>
  <div class="quiz-tabs">
    <div class="quiz-tab">Q1 <div class="quiz-popup">...</div></div>
  </div>
</div>
```

**Quiz Structure**:
- 3 questions per paper (`question1`, `question2`, `question3`)
- 4 options each (`option1`-`option4`)
- Answer stored in `data-answer` attribute
- Click choice → immediate feedback (correct/incorrect)

## Critical Implementation Details

### Unicode Handling in Search
PDF text contains surrogate pairs and mathematical symbols that cause encoding errors. **Always** use `clean_text()` before:
- Splitting text into chunks
- Embedding generation
- Saving to JSONL/SQLite

```python
def clean_text(text: str) -> str:
    """Remove surrogate pairs, math symbols, control chars"""
    text = re.sub(r'[\ud800-\udfff]', '', text)          # Surrogate pairs
    text = re.sub(r'[\U0001D400-\U0001D7FF]', '?', text) # Math symbols
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)  # Control chars
    return text.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
```

### Personal Notes Integration
Notes from `dailies/notes/{date}.md` are integrated in TWO places:
1. **HTML pages**: Loaded in `daily_papers.py` via subpage template
2. **Vector index**: Added to metadata in `build_index.py` via `create_chunks_from_paper()`

```python
# In build_index.py:create_chunks_from_paper()
date_added = metadata['date_added']
notes_file = Path('dailies') / 'notes' / f'{date_added}.md'
if notes_file.exists():
    personal_notes = notes_file.read_text('utf-8').strip()
    metadata['personal_notes'] = clean_text(personal_notes)
```

### FAISS Index vs Embeddings Storage
- **Embeddings**: Stored in shards (`embeddings/shard_*.pkl`) - REUSABLE
- **FAISS Index**: Built from embeddings (`index.faiss`) - REBUILDABLE

To change FAISS index type (Flat → HNSW → IVF) without re-downloading PDFs:
```bash
python rebuild_faiss.py --index-dir ... --faiss-type HNSW
```

This rebuilds `index.faiss` from existing `embeddings/` shards.

### AI Assistant Typing Indicator Bug (FIXED)
**Problem**: AI avatar appeared twice when responding

**Root cause** (ai-assistant.js:812-819, 905-915):
```javascript
// WRONG: Only removes content div, leaves avatar
const typingIndicator = this.elements.messages.querySelector('.ai-message__typing');
DOMUtils.removeElement(typingIndicator);

// CORRECT: Remove entire message container
const typingContent = this.elements.messages.querySelector('.ai-message__typing');
const messageDiv = typingContent.closest('.ai-message');
DOMUtils.removeElement(messageDiv);
```

### Git Workflow in daily_papers.py
Main script **automatically**:
1. `git switch main`
2. `git pull`
3. Process papers
4. `git add index.html dailies/ summaries.jsonl`
5. `git commit -m "Daily Paper Push"`
6. `git push origin main`

Skip push with `TEST=TRUE` in `.env`.

## Data Schema Reference

### summaries.jsonl
```json
{
  "title": "Paper Title",
  "published_at": "2024-01-15",           // arXiv publication date
  "url": "https://arxiv.org/pdf/2401.xxxxx",
  "content": "AI-generated summary...",
  "questions": {
    "question1": {"question": "...", "option1-4": "...", "answer": "option2"},
    "question2": {...},
    "question3": {...}
  },
  "flow_chart": "<svg>...</svg>",
  "date": "2024-01-15"                    // Date added to our database
}
```

### Vector Index Metadata
Available in FAISS chunks (query via `/metadata_fields`):
- **Standard**: `title`, `published_at`, `url`, `content`
- **Chunking**: `chunk_index`, `chunk_source` (summary|pdf_original), `total_chunks`
- **Custom**: `date_added` (when added to our DB), `personal_notes` (from dailies/notes/)
- **Optional**: `pdf_pages`, `questions`, `flow_chart`

### SQLite Schema
```sql
CREATE TABLE papers (
  title TEXT PRIMARY KEY,
  published_at TEXT,              -- arXiv publication date
  url TEXT,
  content TEXT,                   -- AI summary
  date_added TEXT,                -- Date added to our database
  personal_notes TEXT             -- From dailies/notes/{date_added}.md
);
```

## Environment Variables

Required in `.env`:
```bash
SPACE_ID=your_google_chat_space_id
KEY=your_google_chat_key
TEST=FALSE                           # Set TRUE to skip git push
GENAI_GATEWAY_API_KEY=your_claude_api_key
```

## Known Issues

### Issue: Index out of sync with summaries.jsonl
**Cause**: New papers added but index not updated
**Fix**: Run `python build_index.py` (incremental update)

### Issue: Personal notes not appearing in search
**Cause**: Notes file path incorrect or index not updated
**Fix**: Ensure `dailies/notes/YYYY-MM-DD.md` exists, then rebuild index

### Issue: Google Chat post fails
**Cause**: Missing environment variables
**Fix**: Check `.env` for `SPACE_ID` and `KEY`

### Issue: PDF download fails
**Cause**: arXiv rate limiting or network issues
**Fix**: Script skips paper and continues (logged in console)

### Issue: Embedding generation hangs
**Cause**: Ollama server not running
**Fix**: Start Ollama server: `ollama serve`

## File Organization

**Generated files** (git-tracked):
- `index.html` - Main page
- `dailies/pages/*.html` - Daily pages
- `summaries.jsonl` - All paper records

**Build artifacts** (git-ignored):
- `vector_indices/` - FAISS indexes
- `papers.sqlite` - SQLite database
- `__pycache__/` - Python bytecode

**User content**:
- `dailies/notes/*.md` - Personal notes (optional, git-tracked)
- `dailies/images/` - Images for notes (optional, git-tracked)

## Architecture Decisions

### Why JSONL instead of database for papers?
- Append-only format (simple)
- Version control with git
- Human-readable for debugging
- SQLite generated on-demand from JSONL

### Why incremental index updates?
- Avoid re-processing all papers (expensive: PDF download + embedding)
- Track processed papers in `processed_papers.json`
- Save embeddings in shards for efficient updates

### Why hybrid search (vector + BM25)?
- Vector: semantic similarity (finds related papers)
- BM25: exact keyword matching (finds specific terms)
- Combined: better recall and precision

### Why two chunk sources per paper?
- `summary`: Concise AI-generated (high quality, focused)
- `pdf_original`: Full paper text (comprehensive, detailed)
- Allows searching both summary and full content

### Why separate localStorage keys for AI assistant?
- Avoid conflicts with personal_page repository
- Different context types (paper vs beer/personal)
- Separate session management per project
