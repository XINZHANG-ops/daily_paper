"""
Configuration for search engine indexing and retrieval.
"""
import hashlib
import json
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class SearchEngineConfig:
    """Configuration for search engine."""

    # Text splitting
    chunk_size: int = 2500
    chunk_overlap: int = 300

    # Embedding model
    embedding_model: str = "embeddinggemma:300m"
    ollama_host: str = "http://localhost:11434"

    # FAISS index type
    faiss_index_type: str = "Flat"  # Options: "Flat" (brute force), "HNSW", "IVF"

    # HNSW parameters (if using HNSW)
    hnsw_m: int = 32  # Number of connections per layer
    hnsw_ef_construction: int = 200  # Size of dynamic candidate list during construction

    # IVF parameters (if using IVF)
    ivf_nlist: int = 100  # Number of clusters

    # Retrieval weights
    vector_weight: float = 0.7
    bm25_weight: float = 0.3

    # Index settings
    index_base_dir: str = "vector_indices"

    def get_config_hash(self) -> str:
        """Generate a hash of the config for folder naming."""
        config_str = f"{self.chunk_size}_{self.chunk_overlap}_{self.embedding_model}"
        return hashlib.md5(config_str.encode()).hexdigest()[:8]

    def get_index_dir(self) -> Path:
        """Get the directory path for this configuration."""
        folder_name = f"chunk{self.chunk_size}_overlap{self.chunk_overlap}_model_{self.embedding_model.replace(':', '_')}"
        return Path(self.index_base_dir) / folder_name

    def save(self, path: Path):
        """Save config to JSON file."""
        with open(path, 'w') as f:
            json.dump(asdict(self), f, indent=2)

    @classmethod
    def load(cls, path: Path) -> 'SearchEngineConfig':
        """Load config from JSON file."""
        with open(path, 'r') as f:
            data = json.load(f)
        return cls(**data)

    def __eq__(self, other):
        """Check if two configs are equal."""
        if not isinstance(other, SearchEngineConfig):
            return False
        return (self.chunk_size == other.chunk_size and
                self.chunk_overlap == other.chunk_overlap and
                self.embedding_model == other.embedding_model)
