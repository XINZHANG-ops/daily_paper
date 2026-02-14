"""Definitions for FAISS vector store."""

from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import loguru
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_core.documents import Document
from langchain_core.vectorstores.base import VectorStore

from langchain_core.embeddings import Embeddings

ALLOWED_DISTANCE_STRATEGY = [
    DistanceStrategy.MAX_INNER_PRODUCT,
    DistanceStrategy.EUCLIDEAN_DISTANCE,
    DistanceStrategy.COSINE,
]


class FaissVectorStore:
    """In-memory FAISS vector store."""

    def __init__(
        self,
        documents: List[Document] | List[Tuple[str, List[float]]],
        embedding_client: Embeddings,
        metadatas: List[Dict] | None,
        distance_strategy: DistanceStrategy = DistanceStrategy.COSINE,
        **kwargs,
    ):
        """Initialize the in-memory FAISS data retriever.

        Documents can be a list of langchain documents. In this case,
        we make embedding API calls to get the vector, and metadata
        is not required as the Documents have metadata.

        Documents can also be text (and corresponding embedding). In
        this case, we will use the provided vectors, but metadata needs
        to be provided as a list of dictionaries.
        """
        if distance_strategy not in ALLOWED_DISTANCE_STRATEGY:
            raise ValueError(
                f"distance_strategy should be one of {ALLOWED_DISTANCE_STRATEGY}, got {distance_strategy}"  # noqa: E501
            )

        VectorStore._max_inner_product_relevance_score_fn = lambda _, y: min(
            max((y + 1) / 2, 0), 1
        )

        self.distance_strategy = distance_strategy
        self.embedding_client = embedding_client

        if documents is None:
            pass
        elif isinstance(documents[0], Document):
            self.db = self.__create_vectorstore_from_docs(
                documents=documents, embedding_client=embedding_client
            )
        elif documents is not None and metadatas is None:
            raise ValueError(
                (
                    "metadatas should not be None when "
                    "documents are not LangChain documents."
                )
            )
        elif documents is not None and metadatas is not None:
            self.db = self.__create_vectorstore_from_embeddings(
                text_embeddings=documents,
                embedding_client=embedding_client,
                metadatas=metadatas,
            )

    def load_local(
        self,
        vector_store_dir: str | Path,
        allow_dangerous_deserialization: bool = True,
        **kwargs,
    ) -> FAISS:
        """Load FAISS vector store from local directory."""
        db = FAISS.load_local(
            vector_store_dir,
            self.embedding_client,
            allow_dangerous_deserialization=allow_dangerous_deserialization,
            distance_strategy=self.distance_strategy,
            **kwargs,
        )
        return db

    def __create_vectorstore_from_embeddings(
        self,
        text_embeddings: Iterable[Tuple[str, List[float]]],
        embedding_client: Embeddings,
        metadatas: Iterable[dict],
    ) -> FAISS:
        """Create vector store with text and embeddings."""
        db = FAISS.from_embeddings(
            text_embeddings=text_embeddings,
            embedding=embedding_client,
            metadatas=metadatas,
            distance_strategy=self.distance_strategy,
        )
        return db

    def __create_vectorstore_from_docs(
        self,
        documents: List[Document],
        embedding_client: Embeddings,
        max_chunk_size: int = 16,
    ) -> FAISS:
        """Create vector store with documents."""
        chunks = [
            documents[i : i + max_chunk_size]
            for i in range(0, len(documents), max_chunk_size)
        ]
        db = FAISS.from_documents(
            chunks[0],
            embedding=embedding_client,
            distance_strategy=self.distance_strategy,
        )
        for chunk in chunks[1:]:
            db_temp = FAISS.from_documents(
                chunk,
                embedding=embedding_client,
                distance_strategy=self.distance_strategy,
            )
            db.merge_from(db_temp)
        return db
