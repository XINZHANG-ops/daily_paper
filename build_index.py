#!/usr/bin/env python3
"""
Build vector database index from summaries.jsonl.

Supports incremental updates - only processes new papers not in the existing index.
"""
import argparse
import json
from pathlib import Path
from typing import List, Dict, Any, Set
from loguru import logger

from ollama import Client
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

from utils.arxiv_utils import download_paper_text
from search_engine_utils.config import SearchEngineConfig


def load_summaries(summaries_file: Path) -> List[Dict[str, Any]]:
    """Load summaries from JSONL file."""
    summaries = []
    with open(summaries_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                summaries.append(json.loads(line))
    return summaries


def get_all_metadata_fields(summaries: List[Dict]) -> Set[str]:
    """Find all unique fields across all summaries."""
    all_fields = set()
    for summary in summaries:
        all_fields.update(summary.keys())
    return all_fields


def extract_arxiv_id(url: str) -> str:
    """Extract arXiv ID from URL."""
    import re
    # Handle both arxiv.org/pdf/XXXX.XXXX and other formats
    match = re.search(r'(\d{4}\.\d+)', url)
    if match:
        return match.group(1)
    return None


def load_processed_papers(index_dir: Path) -> Set[str]:
    """Load the set of already processed paper URLs."""
    processed_file = index_dir / "processed_papers.json"
    if processed_file.exists():
        with open(processed_file, 'r') as f:
            data = json.load(f)
            return set(data.get('processed_urls', []))
    return set()


def save_processed_papers(index_dir: Path, processed_urls: Set[str]):
    """Save the set of processed paper URLs."""
    processed_file = index_dir / "processed_papers.json"
    with open(processed_file, 'w') as f:
        json.dump({'processed_urls': list(processed_urls)}, f, indent=2)


def create_chunks_from_paper(
    summary: Dict[str, Any],
    config: SearchEngineConfig,
    all_fields: Set[str]
) -> List[Document]:
    """
    Create document chunks from a paper.

    Chunks both the original PDF text and the summary content.
    """
    documents = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap
    )

    # Create metadata with all possible fields (None if missing)
    metadata = {field: summary.get(field, None) for field in all_fields}

    url = summary.get('url', '')
    arxiv_id = extract_arxiv_id(url)

    # Chunk 1: Summary content (already concise, AI-generated)
    summary_content = summary.get('content', '')
    if summary_content:
        chunks = text_splitter.split_text(summary_content)
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk,
                metadata={
                    **metadata,
                    'chunk_index': i,
                    'chunk_source': 'summary',
                    'total_chunks': len(chunks)
                }
            )
            documents.append(doc)

    # Chunk 2: Original PDF text (if arxiv_id available)
    if arxiv_id:
        logger.info(f"Downloading PDF for {arxiv_id}")
        result = download_paper_text(arxiv_id)

        if result['success']:
            pdf_text = result['text']
            chunks = text_splitter.split_text(pdf_text)
            logger.info(f"Created {len(chunks)} chunks from PDF")

            for i, chunk in enumerate(chunks):
                doc = Document(
                    page_content=chunk,
                    metadata={
                        **metadata,
                        'chunk_index': i,
                        'chunk_source': 'pdf_original',
                        'total_chunks': len(chunks),
                        'pdf_pages': result.get('pages', 0)
                    }
                )
                documents.append(doc)
        else:
            logger.warning(f"Failed to download PDF for {arxiv_id}: {result['message']}")

    return documents


def build_index(
    summaries_file: Path = Path("summaries.jsonl"),
    config: SearchEngineConfig = None,
    force_rebuild: bool = False,
    batch_size: int = 3
):
    """
    Build or update the vector database index.

    Args:
        summaries_file: Path to summaries JSONL file
        config: Search engine configuration
        force_rebuild: If True, rebuild from scratch instead of incremental update
        batch_size: Number of papers to process before saving (default: 3)
    """
    if config is None:
        config = SearchEngineConfig()

    # Create index directory
    index_dir = config.get_index_dir()
    index_dir.mkdir(parents=True, exist_ok=True)

    # Save config
    config.save(index_dir / "config.json")
    logger.info(f"Index directory: {index_dir}")

    # Load summaries
    summaries = load_summaries(summaries_file)
    all_fields = get_all_metadata_fields(summaries)
    logger.info(f"Loaded {len(summaries)} papers from {summaries_file}")
    logger.info(f"Found {len(all_fields)} unique metadata fields: {all_fields}")

    # Load processed papers
    if force_rebuild:
        processed_urls = set()
        logger.info("Force rebuild mode - processing all papers")
        # Delete existing index if force rebuild
        index_file = index_dir / "index.faiss"
        if index_file.exists():
            import shutil
            shutil.rmtree(index_dir)
            index_dir.mkdir(parents=True, exist_ok=True)
            config.save(index_dir / "config.json")
    else:
        processed_urls = load_processed_papers(index_dir)
        logger.info(f"Already processed {len(processed_urls)} papers")

    # Find new papers to process
    new_summaries = [s for s in summaries if s.get('url') not in processed_urls]
    logger.info(f"Found {len(new_summaries)} new papers to process")

    if not new_summaries:
        logger.info("No new papers to process. Index is up to date.")
        return

    # Initialize embedding client
    embedding_client = OllamaEmbeddings(
        model=config.embedding_model,
        base_url=config.ollama_host
    )

    # Load or initialize FAISS index
    index_file = index_dir / "index.faiss"
    db = None
    if index_file.exists():
        logger.info("Loading existing index...")
        db = FAISS.load_local(
            str(index_dir),
            embedding_client,
            allow_dangerous_deserialization=True
        )

    # Process papers in batches
    embedding_batch_size = 16  # For FAISS embedding creation
    total_processed = 0

    for batch_start in range(0, len(new_summaries), batch_size):
        batch = new_summaries[batch_start:batch_start + batch_size]
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing batch {batch_start//batch_size + 1}/{(len(new_summaries)-1)//batch_size + 1}")
        logger.info(f"Papers {batch_start+1}-{min(batch_start+batch_size, len(new_summaries))} of {len(new_summaries)}")
        logger.info(f"{'='*60}")

        batch_documents = []

        # Process each paper in the batch
        for summary in batch:
            title = summary.get('title', 'unknown')
            url = summary.get('url', '')

            try:
                logger.info(f"Processing: {title}")
                docs = create_chunks_from_paper(summary, config, all_fields)

                if docs:
                    batch_documents.extend(docs)
                    processed_urls.add(url)
                    total_processed += 1
                    logger.info(f"✓ Created {len(docs)} chunks")
                else:
                    logger.warning(f"⚠ No chunks created for {title}")

            except Exception as e:
                logger.error(f"✗ Error processing {title}: {e}")
                import traceback
                logger.error(traceback.format_exc())
                continue

        # Save batch to index
        if batch_documents:
            logger.info(f"\nAdding {len(batch_documents)} chunks to index...")

            if db is None:
                # Create initial index
                logger.info("Creating new index...")
                chunks = [batch_documents[i:i+embedding_batch_size]
                         for i in range(0, len(batch_documents), embedding_batch_size)]

                db = FAISS.from_documents(chunks[0], embedding_client)
                for chunk in chunks[1:]:
                    db_temp = FAISS.from_documents(chunk, embedding_client)
                    db.merge_from(db_temp)
            else:
                # Merge into existing index
                chunks = [batch_documents[i:i+embedding_batch_size]
                         for i in range(0, len(batch_documents), embedding_batch_size)]

                for chunk in chunks:
                    db_temp = FAISS.from_documents(chunk, embedding_client)
                    db.merge_from(db_temp)

            # Save index after each batch
            logger.info(f"Saving index to {index_dir}...")
            db.save_local(str(index_dir))

            # Save processed papers log after each batch
            save_processed_papers(index_dir, processed_urls)

            logger.info(f"✓ Batch saved! Total papers processed so far: {len(processed_urls)}")
        else:
            logger.warning("No documents in this batch to save")

    logger.info(f"\n{'='*60}")
    logger.info(f"✓ Index built successfully!")
    logger.info(f"Total papers processed: {len(processed_urls)}")
    logger.info(f"New papers added: {total_processed}")
    logger.info(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(description="Build vector database index from papers")
    parser.add_argument(
        '--summaries',
        type=Path,
        default=Path('summaries.jsonl'),
        help='Path to summaries JSONL file (default: summaries.jsonl)'
    )
    parser.add_argument(
        '--chunk-size',
        type=int,
        default=2500,
        help='Chunk size for text splitting (default: 2500)'
    )
    parser.add_argument(
        '--chunk-overlap',
        type=int,
        default=300,
        help='Chunk overlap for text splitting (default: 300)'
    )
    parser.add_argument(
        '--embedding-model',
        type=str,
        default='embeddinggemma:300m',
        help='Ollama embedding model (default: embeddinggemma:300m)'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=3,
        help='Number of papers to process before saving (default: 3)'
    )
    parser.add_argument(
        '--force-rebuild',
        action='store_true',
        help='Force rebuild from scratch instead of incremental update'
    )

    args = parser.parse_args()

    config = SearchEngineConfig(
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        embedding_model=args.embedding_model
    )

    build_index(
        summaries_file=args.summaries,
        config=config,
        force_rebuild=args.force_rebuild,
        batch_size=args.batch_size
    )


if __name__ == '__main__':
    main()
