#!/usr/bin/env python3
"""
Serve vector search API with Flask.

Loads a pre-built FAISS index and provides search endpoints.
Also provides SQLite database query endpoints for papers.
"""
import argparse
import re
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

    # Start Flask server
    logger.info(f"Starting server on {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == '__main__':
    main()
