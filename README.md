# Daily Paper

An automated system for fetching, summarizing, and publishing daily AI research papers.

https://xinzhang-ops.github.io/daily_paper/

https://xinzhang-ops.github.io/daily_paper/dailies/pages/2026-01-02.html

## 🎯 Features

- **Automated Paper Fetching**: Pulls top papers from HuggingFace daily
- **AI-Powered Summaries**: Uses Claude AI to generate 5-point structured summaries
- **Interactive Quizzes**: Auto-generated questions to test understanding
- **Visual Flowcharts**: SVG diagrams showing paper methodology
- **Personal Takeaways**: Add your own notes in markdown
- **Multi-Platform**: Posts to Google Chat + generates GitHub Pages website
- **🤖 AI Chat Assistant**: Integrated AI assistant for asking questions about papers

## 📁 Repository Structure

```
daily_paper/
├── dailies/
│   ├── pages/          # Generated HTML files (159 pages)
│   ├── notes/          # Your markdown takeaways (optional)
│   └── images/         # Images for your notes
├── bg/                 # Background images for papers
├── daily_papers.py     # Main script
├── daily_paper_utils.py # Utility functions
├── html_temps.py       # HTML templates
├── models.py           # AI model interface
└── summaries.jsonl     # Archive of all papers (5.2 MB)
```

## 🚀 Quick Start

### Running the Daily Script

```bash
python daily_papers.py
```

This will:
1. Fetch top 3 papers from HuggingFace
2. Download and analyze PDFs
3. Generate summaries, quizzes, and flowcharts
4. Post to Google Chat
5. Update GitHub Pages
6. Commit and push to git

### Adding Personal Notes

Want to add your own thoughts to a day's papers?

1. Create a markdown file:
   ```bash
   nano dailies/notes/2026-01-02.md
   ```

2. Write your notes:
   ```markdown
   # My Takeaways

   - Key insight 1
   - Key insight 2

   ![My diagram](diagram.png)
   ```

3. Add images (optional):
   ```bash
   mkdir dailies/images/2026-01-02
   cp your-image.png dailies/images/2026-01-02/
   ```

4. Re-run the script - your notes appear automatically!

See [QUICK_START.md](QUICK_START.md) for details.

## 📚 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Quick reference for adding takeaways
- **[TAKEAWAYS_GUIDE.md](TAKEAWAYS_GUIDE.md)** - Complete guide with examples
- **[CHANGES_SUMMARY.md](CHANGES_SUMMARY.md)** - Technical implementation details

## 🔧 Configuration

Set these environment variables in `.env`:

```
SPACE_ID=your_google_chat_space_id
KEY=your_google_chat_key
TEST=FALSE  # Set to TRUE to skip git push
```

## 📊 What You Get

### Daily HTML Pages
Each day's page includes:
- 3 AI-generated paper summaries
- Interactive quiz questions (3 per paper)
- Visual flowcharts of methodologies
- Your personal takeaways (if you add them)

### Example
Visit: `https://xinzhang-ops.github.io/daily_paper/dailies/pages/2026-01-02.html`

## 🛠️ Dependencies

```bash
pip install markdown requests pypdf loguru httplib2 python-dotenv
```

## 📈 Stats

- **159** days of papers tracked
- **5.2 MB** of paper summaries
- **Date range**: March 20, 2025 - January 2, 2026

## 🎨 Features Detail

### AI Summaries
Each paper is analyzed for:
1. 📘 Topic and Domain
2. 💡 Previous Research and New Ideas
3. ❓ Problem
4. 🛠️ Methods
5. 📊 Results and Evaluation

### Quiz System
- 3 multiple-choice questions per paper
- Instant feedback
- Tests comprehension of key concepts

### Personal Notes
- Write in simple markdown
- Supports all markdown features
- Beautiful purple gradient styling
- Images automatically sized and styled

## 🔍 Search Engine & Database

The repository includes both vector search (FAISS) and SQL query capabilities.

### Vector Search Index Metadata

Each paper chunk includes these metadata fields:

**Standard Fields:**
- **title**: Paper title
- **published_at**: Original publication date from arXiv
- **url**: Link to the paper PDF
- **content**: AI-generated summary
- **chunk_index**: Index of the text chunk
- **chunk_source**: Origin of chunk (`summary` or `pdf_original`)
- **total_chunks**: Total number of chunks for this paper

**Custom Fields:**
- **date_added**: The date when the paper was added to our database (from `date` field in `summaries.jsonl`)
- **personal_notes**: Personal notes written by Xin (loaded from `dailies/notes/{date_added}.md` if exists, otherwise `None`)

### SQLite Database Schema

The SQLite database (`papers.sqlite`) provides structured SQL queries:

| Column | Type | Description |
|--------|------|-------------|
| `title` | TEXT | Paper title (PRIMARY KEY) |
| `published_at` | TEXT | Publication date (YYYY-MM-DD) |
| `url` | TEXT | arXiv link to the paper |
| `content` | TEXT | Paper summary/abstract |
| `date_added` | TEXT | Date when paper was added to our database |
| `personal_notes` | TEXT | Personal notes written by Xin |

### Rebuilding the Database

To rebuild the SQLite database with new fields:

```bash
# Rebuild with --overwrite-db flag
python serve_search.py \
  --index-dir vector_indices/your_index \
  --summaries-path summaries.jsonl \
  --sqlite-path papers.sqlite \
  --overwrite-db \
  --port 5001
```

This will:
- Read all papers from `summaries.jsonl`
- Load personal notes from `dailies/notes/{date_added}.md` for each paper
- Create/recreate the SQLite database with all fields

### Using the Search API

Query the database via the `/query` endpoint:

```bash
# Get papers with personal notes
curl -X POST http://localhost:5001/query \
  -H "Content-Type: application/json" \
  -d '{"sql": "SELECT * FROM papers WHERE personal_notes IS NOT NULL LIMIT 10"}'

# Get papers added in a specific date range
curl -X POST http://localhost:5001/query \
  -H "Content-Type: application/json" \
  -d '{"sql": "SELECT title, date_added FROM papers WHERE date_added >= \"2026-02-01\" ORDER BY date_added DESC"}'
```

## 🤖 AI Chat Assistant

An integrated AI assistant is available on both the main page and all paper subpages:

### Features
- **Paper Context**: Automatically tagged with 📄 paper context
- **Date Awareness**: On subpages, the assistant knows which date's papers you're viewing
- **Persistent Sessions**: Chat history persists across page navigations
- **Shared Backend**: Uses the same AI backend as personal_page repository

### Usage
1. Click the robot icon (🤖) in the bottom right corner
2. The assistant automatically knows you're asking about papers
3. On specific date pages (e.g., `2026-02-13.html`), it knows the exact date
4. Type `@` to see available context options (only "paper" for this repo)
5. Use backspace to remove the context tag if needed

### Technical Details
- **Frontend Files**:
  - `js/ai-assistant-*.js` - Core chat functionality
  - `css/ai-assistant.css` - Styling
- **Backend**: Shared endpoint configured in `js/ai-assistant-config.js`
- **Storage**: Uses localStorage to persist chat state and sessions (separate keys from personal_page)
- **Paper Date Detection**: Automatically extracts date from URL path or page title
- **Session Management**: Each page visit uses a unique session ID to maintain conversation context

### Configuration
The assistant connects to the same backend as personal_page:
- **Local**: `http://localhost:8080/chat`
- **GitHub Pages**: Uses ngrok tunnel (configure in `js/ai-assistant-config.js`)
- **Backend Communication**: Sends `context_type: "paper"` and `paper_date` (if on subpage) with each request

## Wiki Knowledge Base

An LLM-maintained wiki at `wiki/` that grows richer with every paper ingested.

**Structure:** `papers/`, `topics/`, `entities/` (models, datasets, algorithms), `ideas/` (cross-cutting insights from personal notes)

**Pipeline:** `wiki_sync.py` stages papers + notes into `wiki/raw/` -> `wiki_build.sh` launches ollama claude agent -> agent creates pages with annotated `[[wikilinks]]`

**Commands:**
```bash
bash wiki_rebuild.sh              # Full rebuild from last 7 days
bash wiki_build.sh                # Incremental build (new papers only)
python wiki_sync.py               # Stage new papers + notes
```

**Query:** The `/ask_wiki` endpoint on `serve_search.py` (port 5001) searches the wiki with session memory, following `[[wikilinks]]` across directories.

## System Architecture

This project is part of a 3-repo system. Mac and Windows are on the same WiFi LAN. Windows runs ngrok to expose port 8080 to the internet for GitHub Pages access.

| Repo | Machine | Role | Port |
|------|---------|------|------|
| **daily_paper** (this) | Mac | Paper wiki + search API | 5001 |
| **Daily-AI-News** | Mac | AI news wiki + search API | 5002 |
| **ai-server** | Windows | Central chat router + ngrok | 8080 |

**Flow:** GitHub Pages → ngrok → Windows ai-server (port 8080) → routes by `context_type` → Mac LAN IP:5001 or :5002.

## Links

- **Live Site**: https://xinzhang-ops.github.io/daily_paper/
- **GitHub**: https://github.com/xinzhang-ops/daily_paper
- **Personal Page**: https://xinzhang-ops.github.io/personal_page/ (shares AI backend)
