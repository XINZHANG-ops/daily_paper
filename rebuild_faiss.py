#!/usr/bin/env python3
"""
Rebuild FAISS index from saved embeddings.

This allows you to change FAISS index type (Flat, HNSW, IVF) without
regenerating embeddings from PDFs.
"""
import argparse
import pickle
from pathlib import Path
from loguru import logger

import faiss
import numpy as np
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

from search_engine_utils.config import SearchEngineConfig
from search_engine_utils.embeddings_manager import EmbeddingsManager


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


def rebuild_index(index_dir: Path, config: SearchEngineConfig = None):
    """
    Rebuild FAISS index from saved embeddings.

    Args:
        index_dir: Directory containing embeddings
        config: New configuration (if None, loads from index_dir)
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
        db = None
        embedding_dim = None

        for i, (batch_text_emb, batch_meta) in enumerate(emb_manager.iter_all_embeddings(batch_size=1000)):
            logger.info(f"Processing batch {i+1} with {len(batch_text_emb)} embeddings...")

            if embedding_dim is None:
                embedding_dim = len(batch_text_emb[0][1])
                logger.info(f"Embedding dimension: {embedding_dim}")

            if db is None:
                # Create initial index with custom type
                custom_index = create_faiss_index(batch_text_emb, config, embedding_dim)

                db = FAISS.from_embeddings(
                    text_embeddings=batch_text_emb,
                    embedding=embedding_client,
                    metadatas=batch_meta,
                    distance_strategy=faiss.METRIC_L2,
                    index=custom_index
                )
            else:
                # Merge batch into existing index
                db_temp = FAISS.from_embeddings(
                    text_embeddings=batch_text_emb,
                    embedding=embedding_client,
                    metadatas=batch_meta
                )
                db.merge_from(db_temp)
    else:
        # Load all at once (legacy mode)
        logger.info(f"Loaded {len(text_embeddings)} embeddings")
        embedding_dim = len(text_embeddings[0][1])
        logger.info(f"Embedding dimension: {embedding_dim}")

        # Create FAISS index with specified type
        custom_index = create_faiss_index(text_embeddings, config, embedding_dim)

        # Build LangChain FAISS from embeddings with custom index
        logger.info("Building LangChain FAISS vector store...")
        db = FAISS.from_embeddings(
            text_embeddings=text_embeddings,
            embedding=embedding_client,
            metadatas=metadatas,
            distance_strategy=faiss.METRIC_L2,
            index=custom_index
        )

    # Save new index
    logger.info(f"Saving rebuilt index to {index_dir}")
    db.save_local(str(index_dir))

    # Update config
    config.save(index_dir / "config.json")

    logger.info(f"✓ Index rebuilt successfully with {config.faiss_index_type} index type!")


def main():
    parser = argparse.ArgumentParser(
        description="Rebuild FAISS index from saved embeddings"
    )
    parser.add_argument(
        '--index-dir',
        type=Path,
        required=True,
        help='Directory containing embeddings.pkl'
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

    rebuild_index(args.index_dir, config)


if __name__ == '__main__':
    main()
