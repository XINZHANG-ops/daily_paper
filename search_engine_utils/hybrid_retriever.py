#!/usr/bin/env python3
"""
Hybrid retrieval combining vector search (FAISS) and keyword search (BM25)
"""

import numpy as np
from typing import List, Tuple, Dict, Any

from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from nltk.tokenize import TreebankWordTokenizer
from rank_bm25 import BM25Okapi

from search_engine_utils.faiss_vectorstore import FaissVectorStore


class HybridRetriever:
    """
    Hybrid retriever combining FAISS vector search and BM25 keyword search.

    Based on the approach from domain_knowledge_retriever.py:
    1. Vector search with similarity threshold filtering
    2. BM25 keyword matching
    3. Score fusion using weighted combination
    4. Return top-k results
    """

    def __init__(
        self,
        documents: List[Document],
        embedding_client: OllamaEmbeddings,
        vector_weight: float = 0.7,
        bm25_weight: float = 0.3,
        similarity_threshold: float = 0.0,  # Minimum similarity score
        faiss_db = None  # Optional: pre-loaded FAISS database
    ):
        """
        Initialize hybrid retriever.

        Args:
            documents: List of Document objects with content and metadata
            embedding_client: Embedding model for vector search
            vector_weight: Weight for vector search scores (default: 0.7)
            bm25_weight: Weight for BM25 scores (default: 0.3)
            similarity_threshold: Minimum similarity threshold for vector search
            faiss_db: Optional pre-loaded FAISS database (to avoid recreating embeddings)
        """
        self.documents = documents
        self.embedding_client = embedding_client
        self.vector_weight = vector_weight
        self.bm25_weight = bm25_weight
        self.similarity_threshold = similarity_threshold

        # Use pre-loaded FAISS db if provided, otherwise create new one
        if faiss_db is not None:
            from loguru import logger
            logger.info("Using pre-loaded FAISS index (skipping embedding generation)")
            self.vector_store = type('obj', (object,), {'db': faiss_db})()
        else:
            from loguru import logger
            logger.info("Creating new FAISS vector store (this may take a while)...")
            # Initialize vector store
            self.vector_store = FaissVectorStore(
                documents=documents,
                embedding_client=embedding_client,
                metadatas=[doc.metadata for doc in documents]
            )

        # Initialize BM25
        self._init_bm25()

    def _init_bm25(self):
        """Initialize BM25 index."""
        from loguru import logger

        # Extract text content from documents
        logger.info(f"Extracting text from {len(self.documents)} documents...")
        self.doc_texts = [doc.page_content for doc in self.documents]

        # Create BM25 index
        logger.info("Tokenizing documents for BM25...")
        self.tokenizer = TreebankWordTokenizer()

        # Show progress for large document sets
        if len(self.doc_texts) > 1000:
            from tqdm import tqdm
            tokenized_docs = [
                self.tokenizer.tokenize(doc.lower())
                for doc in tqdm(self.doc_texts, desc="Tokenizing for BM25")
            ]
        else:
            tokenized_docs = [
                self.tokenizer.tokenize(doc.lower())
                for doc in self.doc_texts
            ]

        logger.info("Building BM25 index...")
        self.bm25 = BM25Okapi(tokenized_docs)
        logger.info("✓ BM25 index ready")

    def _get_ranks_from_scores(self, scores: List[float]) -> np.ndarray:
        """
        Convert scores to ranks (higher score = lower rank number).
        Rank 1 is the best.
        """
        arr = np.array(scores)
        sorted_indices = np.argsort(-arr)  # Sort descending
        ranks = np.empty_like(sorted_indices)
        ranks[sorted_indices] = np.arange(len(arr))
        return ranks + 1  # 1-indexed ranks

    def similarity_search(
        self,
        query: str,
        k: int = 5,
        return_scores: bool = False
    ) -> List[Document] | List[Tuple[Document, float]]:
        """
        Hybrid similarity search combining vector and BM25.

        Args:
            query: Search query
            k: Number of results to return
            return_scores: Whether to return scores with documents

        Returns:
            List of documents or list of (document, score) tuples
        """
        # Step 1: Vector search with all documents
        vector_results = self.vector_store.db.similarity_search_with_score(
            query,
            k=len(self.documents)  # Get all for filtering
        )

        # Filter by similarity threshold
        filtered_results = [
            (doc, score) for doc, score in vector_results
            if score >= self.similarity_threshold
        ]

        if not filtered_results:
            return [] if return_scores else []

        # Create mapping from content to document
        content_to_doc = {doc.page_content: doc for doc, _ in filtered_results}
        doc_contents = list(content_to_doc.keys())

        # Step 2: Calculate vector scores (using ranks)
        vector_ranks = np.arange(len(doc_contents)) + 1
        vector_scores = 1 / vector_ranks

        # Step 3: Calculate BM25 scores
        tokenized_query = self.tokenizer.tokenize(query.lower())
        bm25_scores_all = self.bm25.get_scores(tokenized_query)

        # Map BM25 scores to filtered documents
        doc_to_index = {content: i for i, content in enumerate(self.doc_texts)}
        bm25_scores = []
        for content in doc_contents:
            idx = doc_to_index.get(content, -1)
            if idx >= 0:
                bm25_scores.append(bm25_scores_all[idx])
            else:
                bm25_scores.append(0.0)

        bm25_scores = np.array(bm25_scores)

        # Convert BM25 scores to ranks then to normalized scores
        if bm25_scores.max() > 0:
            bm25_ranks = self._get_ranks_from_scores(bm25_scores)
            bm25_norm_scores = 1 / bm25_ranks
        else:
            bm25_norm_scores = np.zeros_like(bm25_scores)

        # Step 4: Combine scores with weights
        combined_scores = (
            self.vector_weight * vector_scores +
            self.bm25_weight * bm25_norm_scores
        )

        # Step 5: Get top-k results
        top_indices = np.argsort(-combined_scores)[:k]

        results = []
        for idx in top_indices:
            doc = content_to_doc[doc_contents[idx]]
            if return_scores:
                results.append((doc, combined_scores[idx]))
            else:
                results.append(doc)

        return results

    def get_relevant_documents(self, query: str, k: int = 5) -> List[Document]:
        """
        Get relevant documents (compatible with LangChain retrievers).

        Args:
            query: Search query
            k: Number of results to return

        Returns:
            List of relevant documents
        """
        return self.similarity_search(query, k=k, return_scores=False)