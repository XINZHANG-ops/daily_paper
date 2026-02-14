"""
Embeddings manager with sharded storage.

Stores embeddings in multiple shard files to avoid loading/saving
huge files repeatedly.
"""
import json
import pickle
from pathlib import Path
from typing import List, Tuple, Iterator
from loguru import logger


class EmbeddingsManager:
    """Manages sharded embedding storage."""

    def __init__(self, index_dir: Path, shard_size: int = 500):
        """
        Initialize embeddings manager.

        Args:
            index_dir: Directory to store embeddings
            shard_size: Number of chunks per shard file (default: 500)
        """
        self.index_dir = Path(index_dir)
        self.embeddings_dir = self.index_dir / "embeddings"
        self.embeddings_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.embeddings_dir / "index.json"
        self.shard_size = shard_size
        self.index_data = self._load_index()

    def _load_index(self) -> dict:
        """Load embeddings index."""
        if self.index_file.exists():
            with open(self.index_file, 'r') as f:
                return json.load(f)
        return {
            'shards': [],
            'total_chunks': 0,
            'shard_size': self.shard_size
        }

    def _save_index(self):
        """Save embeddings index."""
        with open(self.index_file, 'w') as f:
            json.dump(self.index_data, f, indent=2)

    def append_embeddings(
        self,
        text_embeddings: List[Tuple[str, List[float]]],
        metadatas: List[dict],
        paper_urls: List[str]
    ):
        """
        Append new embeddings to storage.

        Fills up existing shards before creating new ones.

        Args:
            text_embeddings: List of (text, embedding) tuples
            metadatas: List of metadata dicts
            paper_urls: List of paper URLs (for tracking)
        """
        remaining_embeddings = text_embeddings
        remaining_metadatas = metadatas
        remaining_urls = paper_urls

        while remaining_embeddings:
            # Check if we have an incomplete shard
            if self.index_data['shards']:
                last_shard = self.index_data['shards'][-1]
                space_left = self.shard_size - last_shard['num_chunks']

                if space_left > 0:
                    # Fill up the last shard
                    to_add = min(space_left, len(remaining_embeddings))
                    logger.info(f"Adding {to_add} embeddings to existing shard {last_shard['id']} ({last_shard['num_chunks']}/{self.shard_size})")

                    # Load existing shard
                    shard_file = self.embeddings_dir / last_shard['file']
                    with open(shard_file, 'rb') as f:
                        shard_data = pickle.load(f)

                    # Append new data
                    shard_data['text_embeddings'].extend(remaining_embeddings[:to_add])
                    shard_data['metadatas'].extend(remaining_metadatas[:to_add])

                    # Save updated shard
                    with open(shard_file, 'wb') as f:
                        pickle.dump(shard_data, f)

                    # Update index
                    last_shard['num_chunks'] += to_add
                    last_shard['papers'] = list(set(last_shard['papers'] + remaining_urls[:to_add]))

                    # Update remaining
                    remaining_embeddings = remaining_embeddings[to_add:]
                    remaining_metadatas = remaining_metadatas[to_add:]
                    remaining_urls = remaining_urls[to_add:]

                    self.index_data['total_chunks'] += to_add
                    self._save_index()

                    logger.info(f"Shard {last_shard['id']} now has {last_shard['num_chunks']} chunks")
                    continue

            # Create new shard if we still have remaining embeddings
            if remaining_embeddings:
                shard_id = len(self.index_data['shards'])
                shard_file = self.embeddings_dir / f"shard_{shard_id:04d}.pkl"

                # Take up to shard_size embeddings
                to_add = min(self.shard_size, len(remaining_embeddings))
                logger.info(f"Creating new shard {shard_id} with {to_add} embeddings")

                # Save new shard
                with open(shard_file, 'wb') as f:
                    pickle.dump({
                        'text_embeddings': remaining_embeddings[:to_add],
                        'metadatas': remaining_metadatas[:to_add]
                    }, f)

                # Update index
                self.index_data['shards'].append({
                    'id': shard_id,
                    'file': shard_file.name,
                    'num_chunks': to_add,
                    'papers': list(set(remaining_urls[:to_add]))
                })

                # Update remaining
                remaining_embeddings = remaining_embeddings[to_add:]
                remaining_metadatas = remaining_metadatas[to_add:]
                remaining_urls = remaining_urls[to_add:]

                self.index_data['total_chunks'] += to_add
                self._save_index()

        logger.info(f"Total chunks: {self.index_data['total_chunks']}")

    def iter_all_embeddings(
        self,
        batch_size: int = 1000
    ) -> Iterator[Tuple[List[Tuple[str, List[float]]], List[dict]]]:
        """
        Iterate over all embeddings in batches.

        Args:
            batch_size: Number of embeddings per batch

        Yields:
            (text_embeddings, metadatas) tuples
        """
        batch_text_embeddings = []
        batch_metadatas = []

        for shard_info in self.index_data['shards']:
            shard_file = self.embeddings_dir / shard_info['file']
            logger.info(f"Loading shard {shard_info['id']}: {shard_file}")

            with open(shard_file, 'rb') as f:
                data = pickle.load(f)

            text_embeddings = data['text_embeddings']
            metadatas = data['metadatas']

            for text_emb, metadata in zip(text_embeddings, metadatas):
                batch_text_embeddings.append(text_emb)
                batch_metadatas.append(metadata)

                if len(batch_text_embeddings) >= batch_size:
                    yield batch_text_embeddings, batch_metadatas
                    batch_text_embeddings = []
                    batch_metadatas = []

        # Yield remaining
        if batch_text_embeddings:
            yield batch_text_embeddings, batch_metadatas

    def get_all_embeddings(self) -> Tuple[List[Tuple[str, List[float]]], List[dict]]:
        """
        Load all embeddings (use with caution for large datasets).

        Returns:
            (text_embeddings, metadatas) tuple
        """
        all_text_embeddings = []
        all_metadatas = []

        for batch_text_emb, batch_meta in self.iter_all_embeddings(batch_size=10000):
            all_text_embeddings.extend(batch_text_emb)
            all_metadatas.extend(batch_meta)

        return all_text_embeddings, all_metadatas

    def get_total_chunks(self) -> int:
        """Get total number of chunks."""
        return self.index_data['total_chunks']

    def exists(self) -> bool:
        """Check if embeddings exist."""
        return len(self.index_data['shards']) > 0
