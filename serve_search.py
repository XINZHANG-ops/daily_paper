#!/usr/bin/env python3
"""
Serve vector search API with Flask.

Loads a pre-built FAISS index and provides search endpoints.
Also provides SQLite database query endpoints for papers.
Also provides wiki-based Q&A via ollama claude agent.
"""
import argparse
import json
import re
import subprocess
import threading
import time
import requests as http_requests
from pathlib import Path
from flask import Flask, request, jsonify
from loguru import logger

from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

from search_engine_utils.config import SearchEngineConfig
from search_engine_utils.hybrid_retriever import HybridRetriever
from search_engine_utils.paper_sqlite import PaperSqliteManager


def clean_text(text: str) -> str:
    """Clean text by removing problematic Unicode characters."""
    if not text:
        return text

    # Remove surrogate pairs
    text = re.sub(r'[\ud800-\udfff]', '', text)
    # Replace mathematical symbols
    text = re.sub(r'[\U0001D400-\U0001D7FF]', '?', text)
    # Remove control characters
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)

    try:
        text = text.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
    except Exception:
        text = text.encode('ascii', errors='ignore').decode('ascii', errors='ignore')

    return text


app = Flask(__name__)

# Global retriever instance
retriever = None
config = None
all_metadata_fields = set()

# Global SQLite manager instance
sqlite_manager = None

# Session storage — persisted to disk so history survives restarts
SESSIONS_DIR = Path(__file__).parent / "wiki_sessions"
SESSIONS_DIR.mkdir(exist_ok=True)
wiki_sessions = {}


def _load_session(session_id):
    """Load session from disk into memory cache if not already loaded."""
    if session_id in wiki_sessions:
        return wiki_sessions[session_id]
    session_file = SESSIONS_DIR / f"{session_id}.json"
    if session_file.exists():
        try:
            wiki_sessions[session_id] = json.loads(session_file.read_text(encoding='utf-8'))
        except Exception:
            wiki_sessions[session_id] = []
    else:
        wiki_sessions[session_id] = []
    return wiki_sessions[session_id]


def _save_session(session_id):
    """Persist session to disk."""
    session_file = SESSIONS_DIR / f"{session_id}.json"
    try:
        session_file.write_text(json.dumps(wiki_sessions[session_id], ensure_ascii=False), encoding='utf-8')
    except Exception as e:
        logger.error(f"Failed to save session {session_id}: {e}")


def init_retriever(index_dir: Path):
    """Initialize the hybrid retriever from index directory."""
    global retriever, config, all_metadata_fields

    # Load config
    config_file = index_dir / "config.json"
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")

    config = SearchEngineConfig.load(config_file)
    logger.info(f"Loaded config: {config}")

    # Initialize embedding client
    embedding_client = OllamaEmbeddings(
        model=config.embedding_model,
        base_url=config.ollama_host
    )

    # Load FAISS index
    logger.info(f"Loading FAISS index from {index_dir}")
    db = FAISS.load_local(
        str(index_dir),
        embedding_client,
        allow_dangerous_deserialization=True
    )

    # Get documents for hybrid retriever
    # Note: FAISS doesn't expose documents directly, but HybridRetriever needs them
    # We'll reconstruct from the index
    logger.info("Extracting documents from FAISS index...")
    documents = []

    # Show progress for large indexes
    total_docs = db.index.ntotal
    if total_docs > 1000:
        from tqdm import tqdm
        for i in tqdm(range(total_docs), desc="Loading documents"):
            doc = db.docstore.search(db.index_to_docstore_id[i])
            documents.append(doc)
            all_metadata_fields.update(doc.metadata.keys())
    else:
        for i in range(total_docs):
            doc = db.docstore.search(db.index_to_docstore_id[i])
            documents.append(doc)
            all_metadata_fields.update(doc.metadata.keys())

    logger.info(f"Loaded {len(documents)} document chunks")
    logger.info(f"Available metadata fields: {all_metadata_fields}")

    # Initialize hybrid retriever
    logger.info("Initializing hybrid retriever (vector + BM25)...")
    retriever = HybridRetriever(
        documents=documents,
        embedding_client=embedding_client,
        vector_weight=config.vector_weight,
        bm25_weight=config.bm25_weight,
        faiss_db=db  # Pass pre-loaded FAISS index to avoid re-embedding
    )

    logger.info("="*60)
    logger.info("✓ Retriever initialized successfully!")
    logger.info(f"  - Vector search: FAISS ({config.faiss_index_type})")
    logger.info(f"  - Keyword search: BM25")
    logger.info(f"  - Total documents: {len(documents)}")
    logger.info("="*60)


def init_sqlite(summaries_path: Path, sqlite_path: Path, overwrite: bool = False):
    """Initialize the SQLite database manager."""
    global sqlite_manager

    logger.info("Initializing SQLite database...")

    if not summaries_path.exists():
        logger.warning(f"Summaries file not found: {summaries_path}")
        logger.warning("SQLite endpoints will not be available")
        return

    sqlite_manager = PaperSqliteManager(
        paper_summaries_path=summaries_path,
        sqlite_path=sqlite_path,
        overwrite=overwrite
    )

    # Get and log stats
    stats = sqlite_manager.get_stats()
    logger.info("="*60)
    logger.info("✓ SQLite database initialized successfully!")
    logger.info(f"  - Total papers: {stats['total_papers']}")
    logger.info(f"  - Date range: {stats['earliest_paper']} to {stats['latest_paper']}")
    logger.info(f"  - Database path: {stats['database_path']}")
    logger.info("="*60)


@app.before_request
def log_request():
    """Log all incoming requests"""
    logger.info(f"→ {request.method} {request.path} from {request.remote_addr}")
    body = request.get_json(silent=True)
    if body:
        logger.info(f"  Request data: {str(body)[:200]}")


@app.after_request
def log_response(response):
    """Log all outgoing responses"""
    logger.info(f"← {request.method} {request.path} → {response.status_code}")
    return response


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'index_loaded': retriever is not None
    })


@app.route('/search', methods=['POST'])
def search():
    """
    Search endpoint.

    Request body:
    {
        "query": "your search query",
        "k": 5,  // optional, default 5
        "return_fields": ["title", "url", "content"],  // optional, return all if not specified
        "return_scores": true  // optional, default true
    }

    Response:
    {
        "query": "your search query",
        "results": [
            {
                "content": "chunk text...",
                "score": 0.85,
                "metadata": {
                    "title": "Paper title",
                    "url": "http://...",
                    ...
                }
            },
            ...
        ]
    }
    """
    if retriever is None:
        return jsonify({'error': 'Retriever not initialized'}), 500

    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({'error': 'Missing query parameter'}), 400

    query = data['query']
    # Clean query text to handle special characters
    query = clean_text(query)

    k = data.get('k', 5)
    return_fields = data.get('return_fields', None)  # None means return all
    return_scores = data.get('return_scores', True)

    try:
        # Perform search
        results = retriever.similarity_search(
            query=query,
            k=k,
            return_scores=True  # Always get scores internally
        )

        # Format results
        formatted_results = []
        for doc, score in results:
            result = {
                'content': doc.page_content,
            }

            if return_scores:
                result['score'] = float(score)

            # Filter metadata fields if specified
            if return_fields:
                filtered_metadata = {
                    field: doc.metadata.get(field)
                    for field in return_fields
                    if field in doc.metadata
                }
                result['metadata'] = filtered_metadata
            else:
                result['metadata'] = doc.metadata

            formatted_results.append(result)

        return jsonify({
            'query': query,
            'k': k,
            'num_results': len(formatted_results),
            'results': formatted_results
        })

    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/metadata_fields', methods=['GET'])
def metadata_fields():
    """Get all available metadata fields."""
    return jsonify({
        'fields': sorted(list(all_metadata_fields))
    })


@app.route('/stats', methods=['GET'])
def stats():
    """Get index statistics."""
    if retriever is None:
        return jsonify({'error': 'Retriever not initialized'}), 500

    return jsonify({
        'total_chunks': len(retriever.documents),
        'metadata_fields': sorted(list(all_metadata_fields)),
        'config': {
            'chunk_size': config.chunk_size,
            'chunk_overlap': config.chunk_overlap,
            'embedding_model': config.embedding_model,
            'vector_weight': config.vector_weight,
            'bm25_weight': config.bm25_weight
        }
    })


@app.route('/schema', methods=['GET'])
def get_schema():
    """
    Get database schema information.

    Response:
    {
        "table_name": "papers",
        "columns": [
            {
                "name": "title",
                "type": "TEXT",
                "description": "paper title"
            },
            ...
        ]
    }
    """
    if sqlite_manager is None:
        return jsonify({'error': 'SQLite database not initialized'}), 500

    return jsonify(PaperSqliteManager.get_schema())


@app.route('/query', methods=['POST'])
def execute_query():
    """
    Execute a SQL query on the papers database.

    Request body:
    {
        "sql": "SELECT * FROM papers WHERE published_at > '2024-01-01' LIMIT 10"
    }

    Response:
    {
        "sql": "SELECT * FROM papers...",
        "num_results": 10,
        "results": [
            {
                "title": "Paper title",
                "published_at": "2024-01-15",
                "url": "https://arxiv.org/...",
                "content": "Paper summary..."
            },
            ...
        ]
    }
    """
    if sqlite_manager is None:
        return jsonify({'error': 'SQLite database not initialized'}), 500

    data = request.get_json()
    if not data or 'sql' not in data:
        return jsonify({'error': 'Missing sql parameter'}), 400

    sql = data['sql']

    # Basic SQL injection protection - only allow SELECT statements
    sql_upper = sql.strip().upper()
    if not sql_upper.startswith('SELECT'):
        return jsonify({'error': 'Only SELECT queries are allowed'}), 400

    # Prevent dangerous SQL operations
    dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE', 'TRUNCATE']
    for keyword in dangerous_keywords:
        if keyword in sql_upper:
            return jsonify({'error': f'Keyword {keyword} is not allowed in queries'}), 400

    try:
        # Execute query
        results = sqlite_manager.query_dict(sql)

        return jsonify({
            'sql': sql,
            'num_results': len(results),
            'results': results
        })

    except Exception as e:
        logger.error(f"Query error: {e}")
        return jsonify({'error': str(e)}), 500


SAFETY_SERVICE_URL = 'http://localhost:5003/filter'


def _filter_pii(text):
    """Filter PII from text via the safety layer service. Returns original on failure."""
    try:
        resp = http_requests.post(
            SAFETY_SERVICE_URL,
            json={'text': text},
            timeout=30
        )
        if resp.ok:
            return resp.json().get('text', text)
    except Exception as e:
        logger.warning(f"Safety filter unavailable: {e}")
    return text


@app.route('/ask_wiki', methods=['POST'])
def ask_wiki():
    """
    Ask a question based on the wiki knowledge base.

    Request body:
    {
        "question": "What are recent advances in diffusion models?",
        "model": "minimax-m2.7:cloud",  // optional, defaults to minimax-m2.7:cloud
        "session_id": "abc123"  // optional, for conversation history
    }

    Response:
    {
        "question": "...",
        "answer": "...",
        "model": "minimax-m2.7:cloud",
        "session_id": "abc123"
    }
    """
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({'error': 'Missing question parameter'}), 400

    question = data['question']
    model = data.get('model', 'minimax-m2.7:cloud')
    session_id = data.get('session_id', None)

    conversation_history = _load_session(session_id) if session_id else []

    # Find repo root (where wiki/ directory is)
    repo_root = Path(__file__).parent
    wiki_dir = repo_root / 'wiki'
    llm_wiki_path = repo_root / 'llm-wiki.md'
    project_schema_path = wiki_dir / 'WIKI.md'

    if not wiki_dir.exists():
        return jsonify({'error': 'wiki/ directory not found'}), 500

    # Read schema files
    try:
        llm_wiki_content = llm_wiki_path.read_text(encoding='utf-8') if llm_wiki_path.exists() else ""
        project_schema_content = project_schema_path.read_text(encoding='utf-8') if project_schema_path.exists() else ""
    except Exception as e:
        logger.error(f"Failed to read schema files: {e}")
        return jsonify({'error': f'Failed to read schema: {str(e)}'}), 500

    # Build conversation history context
    history_context = ""
    if conversation_history:
        history_context = "\n=== CONVERSATION HISTORY ===\n"
        for msg in conversation_history[-6:]:  # Last 3 turns (6 messages)
            role_label = "User" if msg['role'] == 'user' else "Assistant"
            history_context += f"{role_label}: {msg['content']}\n\n"
        history_context += "=== END HISTORY ===\n\n"

    # Build the prompt for the agent
    prompt = f"""You are a research assistant helping answer questions based on a wiki knowledge base.

=== WIKI PATTERN (llm-wiki.md) ===
{llm_wiki_content}

=== PROJECT SCHEMA (WIKI.md) ===
{project_schema_content}

=== AVAILABLE TOOLS ===

You have access to the following tools running on localhost:5001:

1. **Vector Search** (semantic similarity via FAISS):
   curl -X POST http://localhost:5001/search \\
     -H "Content-Type: application/json" \\
     -d '{{"query": "your search query", "k": 5, "return_scores": true}}'

   Returns: {{"results": [{{"content": "...", "metadata": {{"title": "...", "url": "...", ...}}, "score": 0.85}}]}}

2. **SQL Query** (structured queries on papers database):
   curl -X POST http://localhost:5001/query \\
     -H "Content-Type: application/json" \\
     -d '{{"sql": "SELECT title, published_at FROM papers WHERE ..."}}'

   Returns: {{"results": [{{"title": "...", "published_at": "...", ...}}]}}

   Available columns: title, published_at, url, content, date_added, personal_notes

3. **Database Schema**:
   curl http://localhost:5001/schema

Use these tools to find relevant papers when the wiki alone doesn't have enough information.
For example:
- Use vector search for semantic queries: "papers about transformers"
- Use SQL for structured filters: "papers published after 2024-01-01"
- Read wiki pages for curated summaries and cross-referenced knowledge

{history_context}=== CURRENT QUESTION ===

Working directory: {repo_root}

The user asks: {question}

Strategy:
1. Consider the conversation history above (if any) for context
2. Read wiki/index.md to see all pages across papers/, topics/, entities/, ideas/
3. Read relevant wiki pages — follow [[wikilinks]] across directories, traversing at least 2 levels of connections
4. The wiki contains personal notes and cross-cutting ideas — use these for richer context
5. If wiki coverage is incomplete, use vector search or SQL to find additional papers
6. Synthesize a comprehensive answer combining wiki knowledge and tool results

Provide a comprehensive answer with citations to specific papers (use [[arxiv_id]] format).

Answer:
"""

    # Call ollama launch claude
    try:
        logger.info(f"Calling ollama claude for question: {question[:60]}...")
        result = subprocess.run(
            [
                'ollama', 'launch', 'claude',
                '--model', model,
                '--yes',
                '--',
                '-p', prompt,
                '--permission-mode', 'dontAsk'
            ],
            capture_output=True,
            text=True,
            cwd=str(repo_root),
            timeout=300  # 5 minutes timeout (agent may use FAISS/SQL tools)
        )

        if result.returncode != 0:
            logger.error(f"ollama claude failed: {result.stderr}")
            return jsonify({'error': f'Agent failed: {result.stderr}'}), 500

        answer = result.stdout.strip()
        logger.info(f"Answer generated ({len(answer)} chars)")

        answer = _filter_pii(answer)

        if session_id:
            wiki_sessions[session_id].append({'role': 'user', 'content': question})
            wiki_sessions[session_id].append({'role': 'assistant', 'content': answer})
            if len(wiki_sessions[session_id]) > 20:
                wiki_sessions[session_id] = wiki_sessions[session_id][-20:]
            _save_session(session_id)

        return jsonify({
            'question': question,
            'answer': answer,
            'model': model,
            'session_id': session_id
        })

    except subprocess.TimeoutExpired:
        logger.error("ollama claude timed out")
        return jsonify({'error': 'Request timed out (5 min limit)'}), 504
    except Exception as e:
        logger.error(f"ask_wiki error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/lint_wiki', methods=['POST'])
def lint_wiki():
    """
    Run wiki health check (lint operation).

    Checks for:
    - Contradictions between pages
    - Stale claims superseded by newer sources
    - Orphan pages with no inbound links
    - Missing concept pages
    - Missing cross-references
    - Data gaps

    Request body (optional):
    {
        "model": "minimax-m2.7:cloud"  // optional
    }

    Response:
    {
        "status": "completed",
        "report": "...",
        "model": "minimax-m2.7:cloud"
    }
    """
    data = request.get_json() or {}
    model = data.get('model', 'minimax-m2.7:cloud')

    # Find repo root
    repo_root = Path(__file__).parent
    wiki_dir = repo_root / 'wiki'
    llm_wiki_path = repo_root / 'llm-wiki.md'
    project_schema_path = wiki_dir / 'WIKI.md'

    if not wiki_dir.exists():
        return jsonify({'error': 'wiki/ directory not found'}), 500

    # Read schema files
    try:
        llm_wiki_content = llm_wiki_path.read_text(encoding='utf-8') if llm_wiki_path.exists() else ""
        project_schema_content = project_schema_path.read_text(encoding='utf-8') if project_schema_path.exists() else ""
    except Exception as e:
        logger.error(f"Failed to read schema files: {e}")
        return jsonify({'error': f'Failed to read schema: {str(e)}'}), 500

    # Build the lint prompt
    prompt = f"""You are maintaining a research paper wiki. Run a health check (lint operation).

=== WIKI PATTERN (llm-wiki.md) ===
{llm_wiki_content}

=== PROJECT SCHEMA (WIKI.md) ===
{project_schema_content}

=== YOUR TASK ===

Working directory: {repo_root}

Run a comprehensive health check on wiki/. Check all 4 directories: papers/, topics/, entities/, ideas/.

STRUCTURAL CHECKS:
1. **Contradictions**: Do different pages make conflicting claims?
2. **Stale content**: Has newer content superseded old claims?
3. **Orphan pages**: Papers not linked from any topic page
4. **Orphan topics/entities/ideas**: Pages with no inbound links
5. **Missing cross-references**: Papers that should be linked but aren't
6. **Broken links**: [[references]] that don't have a corresponding page
7. **Metadata consistency**: paper_count vs actual papers in topic pages
8. **Data gaps**: Missing fields, incomplete summaries

CONNECTION QUALITY CHECKS:
9. **Shallow links**: Find connections that just say "Related:", "See also:", or link without annotation → REWRITE with WHY
10. **Missing cross-connections**: Papers that share 2+ entities but have no direct connection → add connection
11. **Topic pages missing ## Evolution**: Write a chronological narrative, not just a paper list
12. **Topic pages missing ## Patterns & Insights**: Synthesize from papers
13. **People in entities/**: Entity pages that are actually about people → flag for removal (entities are for technical things only)

LEARN FROM CHAT HISTORY:
14. Read JSON files in wiki_sessions/ (each is a JSON array of [{{"role":"user","content":"..."}}, ...])
15. Find questions that reveal gaps in the wiki → fill those gaps
16. Find insights from Q&A worth adding to topic/entity/idea pages
17. Find repeated questions → that page needs more depth
Do NOT copy raw Q&A. Extract useful knowledge and integrate naturally.

Read wiki/index.md, then systematically check all pages in papers/, topics/, entities/, ideas/.

After identifying issues:
1. Report all problems found
2. Fix what you can (update pages, add missing links, correct counts, rewrite shallow connections)
3. Update wiki/log.md with a lint entry

Provide a summary report of what you found and fixed.
"""

    # Call ollama launch claude
    try:
        logger.info("Running wiki lint operation...")
        result = subprocess.run(
            [
                'ollama', 'launch', 'claude',
                '--model', model,
                '--yes',
                '--',
                '-p', prompt,
                '--permission-mode', 'dontAsk'
            ],
            capture_output=True,
            text=True,
            cwd=str(repo_root),
            timeout=600  # 10 minutes timeout for lint
        )

        if result.returncode != 0:
            logger.error(f"ollama claude failed: {result.stderr}")
            return jsonify({'error': f'Lint failed: {result.stderr}'}), 500

        report = result.stdout.strip()
        logger.info(f"Lint completed ({len(report)} chars)")

        return jsonify({
            'status': 'completed',
            'report': report,
            'model': model
        })

    except subprocess.TimeoutExpired:
        logger.error("ollama claude timed out during lint")
        return jsonify({'error': 'Lint timed out (10 min limit)'}), 504
    except Exception as e:
        logger.error(f"lint_wiki error: {e}")
        return jsonify({'error': str(e)}), 500


def run_daily_lint():
    """Background thread that runs wiki lint every day."""
    DAY_SECONDS = 24 * 60 * 60

    while True:
        try:
            time.sleep(DAY_SECONDS)
            logger.info("Running scheduled daily wiki lint...")

            repo_root = Path(__file__).parent
            wiki_dir = repo_root / 'wiki'

            if not wiki_dir.exists():
                logger.warning("wiki/ directory not found, skipping scheduled lint")
                continue

            llm_wiki_path = repo_root / 'llm-wiki.md'
            project_schema_path = wiki_dir / 'WIKI.md'

            llm_wiki_content = llm_wiki_path.read_text(encoding='utf-8') if llm_wiki_path.exists() else ""
            project_schema_content = project_schema_path.read_text(encoding='utf-8') if project_schema_path.exists() else ""

            prompt = f"""You are maintaining a research paper wiki. Run a daily health check (lint operation).

=== WIKI PATTERN (llm-wiki.md) ===
{llm_wiki_content}

=== PROJECT SCHEMA (WIKI.md) ===
{project_schema_content}

=== YOUR TASK ===

Working directory: {repo_root}

This is a scheduled daily health check. Run a comprehensive check on wiki/.
Check all 4 directories: papers/, topics/, entities/, ideas/.

STRUCTURAL:
1. Contradictions between pages
2. Stale content superseded by newer sources
3. Orphan pages (no inbound links) across all directories
4. Missing cross-references
5. Broken [[wikilinks]]
6. Metadata consistency (paper_count vs actual)

CONNECTION QUALITY:
7. Shallow connections that just say "Related:" or "See also:" → rewrite with WHY
8. Papers sharing 2+ entities but not connected → add connections
9. Topic pages missing ## Evolution or ## Patterns & Insights → add them
10. People appearing in entities/ → flag (entities are for technical things only)

LEARN FROM CHAT HISTORY:
11. Read JSON files in wiki_sessions/ (each is a JSON array of {{role, content}} messages)
12. Find questions that reveal gaps in the wiki → fill those gaps with new content
13. Find insights or connections from Q&A worth adding to topic/entity/idea pages
14. Find repeated questions about the same subject → that page needs more depth

Do NOT copy raw Q&A into the wiki. Extract useful knowledge and integrate it naturally.

Fix what you can, and update wiki/log.md with a lint entry noting this was a scheduled daily check.

Provide a summary report.
"""

            result = subprocess.run(
                [
                    'ollama', 'launch', 'claude',
                    '--model', 'minimax-m2.7:cloud',
                    '--yes',
                    '--',
                    '-p', prompt,
                    '--permission-mode', 'dontAsk'
                ],
                capture_output=True,
                text=True,
                cwd=str(repo_root),
                timeout=600
            )

            if result.returncode == 0:
                logger.info(f"Daily lint completed successfully ({len(result.stdout)} chars)")
            else:
                logger.error(f"Daily lint failed: {result.stderr}")

        except Exception as e:
            logger.error(f"Error in daily lint thread: {e}")


def main():
    parser = argparse.ArgumentParser(description="Serve vector search and SQL query API")
    parser.add_argument(
        '--index-dir',
        type=Path,
        required=True,
        help='Path to index directory (e.g., vector_indices/chunk2500_overlap300_model_embeddinggemma_300m)'
    )
    parser.add_argument(
        '--summaries-path',
        type=Path,
        default=None,
        help='Path to summaries.jsonl file (default: auto-detect from project root)'
    )
    parser.add_argument(
        '--sqlite-path',
        type=Path,
        default=Path('papers.sqlite'),
        help='Path to SQLite database file (default: papers.sqlite)'
    )
    parser.add_argument(
        '--overwrite-db',
        action='store_true',
        help='Recreate SQLite database from summaries.jsonl'
    )
    parser.add_argument(
        '--host',
        type=str,
        default='0.0.0.0',
        help='Host to bind to (default: 0.0.0.0)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=5001,
        help='Port to bind to (default: 5001)'
    )

    args = parser.parse_args()

    if not args.index_dir.exists():
        logger.error(f"Index directory not found: {args.index_dir}")
        return

    # Initialize retriever
    init_retriever(args.index_dir)

    # Initialize SQLite database
    # Auto-detect summaries.jsonl path if not specified
    if args.summaries_path is None:
        # Try to find summaries.jsonl in parent directories
        current_dir = Path.cwd()
        for parent in [current_dir] + list(current_dir.parents):
            summaries_path = parent / 'summaries.jsonl'
            if summaries_path.exists():
                logger.info(f"Auto-detected summaries.jsonl at: {summaries_path}")
                args.summaries_path = summaries_path
                break

    if args.summaries_path and args.summaries_path.exists():
        init_sqlite(
            summaries_path=args.summaries_path,
            sqlite_path=args.sqlite_path,
            overwrite=args.overwrite_db
        )
    else:
        logger.warning("Summaries file not found. SQLite endpoints will not be available.")
        logger.warning("Use --summaries-path to specify the path to summaries.jsonl")

    # Start daily lint background thread
    logger.info("Starting daily lint background thread...")
    lint_thread = threading.Thread(target=run_daily_lint, daemon=True)
    lint_thread.start()

    # Start Flask server
    logger.info(f"Starting server on {args.host}:{args.port}")
    logger.info("  - POST /search - Hybrid search")
    logger.info("  - POST /query - SQL queries")
    logger.info("  - POST /ask_wiki - Wiki-based Q&A")
    logger.info("  - POST /lint_wiki - Wiki health check (manual)")
    logger.info("  - Daily automated lint enabled")
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == '__main__':
    main()
