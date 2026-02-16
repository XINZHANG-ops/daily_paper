#!/usr/bin/env python3
"""
Rebuild FAISS index from saved embeddings.

This allows you to change FAISS index type (Flat, HNSW, IVF) without
regenerating embeddings from PDFs.

Can also update metadata without recalculating embeddings.
"""
import argparse
import json
import pickle
from pathlib import Path
from loguru import logger

import faiss
import numpy as np
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_core.documents import Document as LCDocument
from langchain_ollama import OllamaEmbeddings

from search_engine_utils.config import SearchEngineConfig
from search_engine_utils.embeddings_manager import EmbeddingsManager


def load_summaries_metadata(summaries_file: Path) -> dict:
    """
    Load metadata from summaries.jsonl and create a lookup by URL.

    Returns:
        dict: Mapping from URL to updated metadata
    """
    url_to_metadata = {}

    with open(summaries_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                paper = json.loads(line)
                url = paper.get('url')
                if url:
                    # Create updated metadata
                    metadata = {
                        'title': paper.get('title'),
                        'published_at': paper.get('published_at'),
                        'url': url,
                        'content': paper.get('content'),
                        'date_added': paper.get('date'),  # The date when paper was added to our DB
                        'personal_notes': None
                    }

                    # Load personal notes if available
                    date_added = metadata['date_added']
                    if date_added:
                        notes_file = Path('dailies') / 'notes' / f'{date_added}.md'
                        if notes_file.exists():
                            try:
                                with open(notes_file, 'r', encoding='utf-8') as nf:
                                    metadata['personal_notes'] = nf.read().strip()
                            except Exception as e:
                                logger.warning(f"Failed to load notes for {date_added}: {e}")

                    url_to_metadata[url] = metadata

    logger.info(f"Loaded metadata for {len(url_to_metadata)} papers from summaries.jsonl")
    return url_to_metadata


def update_metadata_from_summaries(metadatas: list, summaries_file: Path) -> list:
    """
    Update metadata list with fresh data from summaries.jsonl.

    Args:
        metadatas: Original metadata list
        summaries_file: Path to summaries.jsonl

    Returns:
        Updated metadata list
    """
    if not summaries_file.exists():
        logger.warning(f"Summaries file not found: {summaries_file}")
        return metadatas

    logger.info(f"Updating metadata from {summaries_file}...")
    url_to_metadata = load_summaries_metadata(summaries_file)

    updated_metadatas = []
    updated_count = 0

    for old_meta in metadatas:
        url = old_meta.get('url')

        if url and url in url_to_metadata:
            # Merge: keep chunk-specific fields, update paper-level fields
            new_meta = old_meta.copy()
            paper_meta = url_to_metadata[url]

            # Update paper-level fields
            for key in ['title', 'published_at', 'url', 'content', 'date_added', 'personal_notes']:
                if key in paper_meta:
                    new_meta[key] = paper_meta[key]

            updated_metadatas.append(new_meta)
            updated_count += 1
        else:
            # Keep original if no match found
            updated_metadatas.append(old_meta)

    logger.info(f"Updated metadata for {updated_count}/{len(metadatas)} chunks")
    return updated_metadatas


def load_embeddings_legacy(index_dir: Path):
    """Load saved embeddings from legacy single file (backward compatibility)."""
    embeddings_file = index_dir / "embeddings.pkl"

    if embeddings_file.exists():
        logger.info(f"Loading embeddings from legacy file: {embeddings_file}")
        with open(embeddings_file, 'rb') as f:
            data = pickle.load(f)
        return data['text_embeddings'], data['metadatas']

    return None, None


def create_faiss_index(
    text_embeddings: list,
    config: SearchEngineConfig,
    embedding_dim: int
) -> faiss.Index:
    """
    Create FAISS index based on configuration.

    Args:
        text_embeddings: List of (text, embedding) tuples
        config: Search engine configuration
        embedding_dim: Dimension of embeddings

    Returns:
        faiss.Index: Configured FAISS index
    """
    if config.faiss_index_type == "Flat":
        logger.info("Creating Flat (brute force) index")
        index = faiss.IndexFlatL2(embedding_dim)

    elif config.faiss_index_type == "HNSW":
        logger.info(f"Creating HNSW index (M={config.hnsw_m}, ef_construction={config.hnsw_ef_construction})")
        index = faiss.IndexHNSWFlat(embedding_dim, config.hnsw_m)
        index.hnsw.efConstruction = config.hnsw_ef_construction

    elif config.faiss_index_type == "IVF":
        logger.info(f"Creating IVF index (nlist={config.ivf_nlist})")
        quantizer = faiss.IndexFlatL2(embedding_dim)
        index = faiss.IndexIVFFlat(quantizer, embedding_dim, config.ivf_nlist)

        # Train the index
        logger.info("Training IVF index...")
        embeddings_array = np.array([emb for _, emb in text_embeddings], dtype=np.float32)
        index.train(embeddings_array)

    else:
        raise ValueError(f"Unknown FAISS index type: {config.faiss_index_type}")

    return index


def rebuild_index(
    index_dir: Path,
    config: SearchEngineConfig = None,
    summaries_file: Path = None,
    update_metadata: bool = False
):
    """
    Rebuild FAISS index from saved embeddings.

    Args:
        index_dir: Directory containing embeddings
        config: New configuration (if None, loads from index_dir)
        summaries_file: Path to summaries.jsonl for metadata updates
        update_metadata: If True, update metadata from summaries.jsonl
    """
    # Load existing config if not provided
    if config is None:
        config_file = index_dir / "config.json"
        if config_file.exists():
            config = SearchEngineConfig.load(config_file)
        else:
            config = SearchEngineConfig()

    # Initialize embeddings manager
    emb_manager = EmbeddingsManager(index_dir)

    # Check for legacy single file (backward compatibility)
    text_embeddings_legacy, metadatas_legacy = load_embeddings_legacy(index_dir)

    if text_embeddings_legacy is not None:
        # Use legacy file
        logger.info(f"Using legacy embeddings file")
        text_embeddings = text_embeddings_legacy
        metadatas = metadatas_legacy
        use_batched = False
    elif emb_manager.exists():
        # Use sharded storage with batched loading
        logger.info(f"Using sharded embeddings storage")
        logger.info(f"Total chunks: {emb_manager.get_total_chunks()}")
        use_batched = True
        text_embeddings = None
        metadatas = None
    else:
        raise FileNotFoundError(
            f"No embeddings found in {index_dir}\n"
            f"Please run build_index.py first to generate embeddings."
        )

    # Initialize embedding client (needed for FAISS wrapper)
    embedding_client = OllamaEmbeddings(
        model=config.embedding_model,
        base_url=config.ollama_host
    )

    if use_batched:
        # Build index in batches (memory efficient)
        logger.info("Building FAISS index in batches (memory efficient)...")

        # First pass: collect all embeddings and metadata
        logger.info("Collecting embeddings from shards...")
        all_text_embeddings = []
        all_metadatas = []
        embedding_dim = None

        for i, (batch_text_emb, batch_meta) in enumerate(emb_manager.iter_all_embeddings(batch_size=5000)):
            logger.info(f"Loading batch {i+1} with {len(batch_text_emb)} embeddings...")

            if embedding_dim is None:
                embedding_dim = len(batch_text_emb[0][1])
                logger.info(f"Embedding dimension: {embedding_dim}")

            all_text_embeddings.extend(batch_text_emb)
            all_metadatas.extend(batch_meta)

        logger.info(f"Total embeddings collected: {len(all_text_embeddings)}")

        # Update metadata from summaries.jsonl if requested
        if update_metadata and summaries_file:
            all_metadatas = update_metadata_from_summaries(all_metadatas, summaries_file)

        # Create custom FAISS index
        custom_index = create_faiss_index(all_text_embeddings, config, embedding_dim)

        # Add embeddings to custom index
        logger.info("Adding embeddings to custom index...")
        texts = [te[0] for te in all_text_embeddings]
        embeddings_array = np.array([te[1] for te in all_text_embeddings], dtype=np.float32)
        custom_index.add(embeddings_array)

        # Create LangChain FAISS wrapper
        logger.info("Creating LangChain FAISS wrapper...")

        # Create docstore with documents
        documents = [LCDocument(page_content=text, metadata=meta)
                    for text, meta in zip(texts, all_metadatas)]

        index_to_id = {i: str(i) for i in range(len(documents))}
        docstore = InMemoryDocstore({str(i): doc for i, doc in enumerate(documents)})

        # Create FAISS instance with custom index
        db = FAISS(
            embedding_function=embedding_client.embed_query,
            index=custom_index,
            docstore=docstore,
            index_to_docstore_id=index_to_id
        )
    else:
        # Load all at once (legacy mode)
        logger.info(f"Loaded {len(text_embeddings)} embeddings")
        embedding_dim = len(text_embeddings[0][1])
        logger.info(f"Embedding dimension: {embedding_dim}")

        # Update metadata from summaries.jsonl if requested
        if update_metadata and summaries_file:
            metadatas = update_metadata_from_summaries(metadatas, summaries_file)

        # Create FAISS index with specified type
        custom_index = create_faiss_index(text_embeddings, config, embedding_dim)

        # Add embeddings to custom index
        logger.info("Adding embeddings to custom index...")
        texts = [te[0] for te in text_embeddings]
        embeddings_array = np.array([te[1] for te in text_embeddings], dtype=np.float32)
        custom_index.add(embeddings_array)

        # Create LangChain FAISS wrapper
        logger.info("Creating LangChain FAISS wrapper...")

        # Create docstore with documents
        documents = [LCDocument(page_content=text, metadata=meta)
                    for text, meta in zip(texts, metadatas)]

        index_to_id = {i: str(i) for i in range(len(documents))}
        docstore = InMemoryDocstore({str(i): doc for i, doc in enumerate(documents)})

        # Create FAISS instance with custom index
        db = FAISS(
            embedding_function=embedding_client.embed_query,
            index=custom_index,
            docstore=docstore,
            index_to_docstore_id=index_to_id
        )

    # Save new index
    logger.info(f"Saving rebuilt index to {index_dir}")
    db.save_local(str(index_dir))

    # Update config
    config.save(index_dir / "config.json")

    logger.info(f"✓ Index rebuilt successfully with {config.faiss_index_type} index type!")


def main():
    parser = argparse.ArgumentParser(
        description="Rebuild FAISS index from saved embeddings (can also update metadata)"
    )
    parser.add_argument(
        '--index-dir',
        type=Path,
        required=True,
        help='Directory containing embeddings'
    )
    parser.add_argument(
        '--summaries',
        type=Path,
        default=Path('summaries.jsonl'),
        help='Path to summaries.jsonl for metadata updates (default: summaries.jsonl)'
    )
    parser.add_argument(
        '--update-metadata',
        action='store_true',
        help='Update metadata from summaries.jsonl (includes date_added and personal_notes)'
    )
    parser.add_argument(
        '--faiss-type',
        type=str,
        choices=['Flat', 'HNSW', 'IVF'],
        default='Flat',
        help='FAISS index type (default: Flat)'
    )
    parser.add_argument(
        '--hnsw-m',
        type=int,
        default=32,
        help='HNSW M parameter (default: 32)'
    )
    parser.add_argument(
        '--hnsw-ef',
        type=int,
        default=200,
        help='HNSW efConstruction parameter (default: 200)'
    )
    parser.add_argument(
        '--ivf-nlist',
        type=int,
        default=100,
        help='IVF nlist parameter (default: 100)'
    )

    args = parser.parse_args()

    if not args.index_dir.exists():
        logger.error(f"Index directory not found: {args.index_dir}")
        return

    # Load existing config and update FAISS settings
    config_file = args.index_dir / "config.json"
    if config_file.exists():
        config = SearchEngineConfig.load(config_file)
    else:
        config = SearchEngineConfig()

    # Update FAISS configuration
    config.faiss_index_type = args.faiss_type
    config.hnsw_m = args.hnsw_m
    config.hnsw_ef_construction = args.hnsw_ef
    config.ivf_nlist = args.ivf_nlist

    rebuild_index(
        index_dir=args.index_dir,
        config=config,
        summaries_file=args.summaries,
        update_metadata=args.update_metadata
    )


if __name__ == '__main__':
    main()
