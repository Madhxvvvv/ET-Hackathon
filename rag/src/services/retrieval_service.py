"""
retrieval_service.py
Service layer for document retrieval.
Wraps the retriever with metadata filtering and confidence scoring.
Future-ready for hybrid BM25 + vector retrieval.
"""

from __future__ import annotations

import time
from typing import Optional

from configs.config import DEFAULT_TOP_K, get_logger
from src.retriever.retriever import retrieve, RetrievedChunk

logger = get_logger(__name__)

CONFIDENCE_THRESHOLD = 0.3


class RetrievalService:
    """Clean retrieval interface for service layer."""

    def search(
        self,
        query: str,
        k: int = DEFAULT_TOP_K,
        category_filter: Optional[str] = None,
        min_confidence: float = CONFIDENCE_THRESHOLD,
    ) -> dict:
        """
        Search the knowledge base for relevant documents.

        Args:
            query: Search query
            k: Number of results to return
            category_filter: Optional source category filter
            min_confidence: Minimum confidence threshold

        Returns:
            Dict with results, sources, and metadata
        """
        start = time.time()

        if not query or not query.strip():
            return {
                "results": [],
                "sources": [],
                "count": 0,
                "confidence": 0.0,
                "latency_seconds": 0.0,
            }

        try:
            chunks: list[RetrievedChunk] = retrieve(query, k=k)

            # filter by confidence
            filtered = [
                c for c in chunks
                if (1.0 - (c.score or 1.0) / 2.0) >= min_confidence
            ]

            # apply category filter if provided
            if category_filter:
                filtered = [
                    c for c in filtered
                    if category_filter.lower() in c.source.lower()
                ]

            sources = list({c.source for c in filtered})
            avg_confidence = (
                sum(1.0 - (c.score or 1.0) / 2.0 for c in filtered) / len(filtered)
                if filtered else 0.0
            )

            elapsed = time.time() - start
            logger.info(
                "Retrieval: %d results in %.2fs | query=%r",
                len(filtered), elapsed, query[:60]
            )

            return {
                "results": [
                    {
                        "content": c.content,
                        "source": c.source,
                        "confidence": round(1.0 - (c.score or 1.0) / 2.0, 3),
                        "metadata": c.metadata,
                    }
                    for c in filtered
                ],
                "sources": sources,
                "count": len(filtered),
                "confidence": round(avg_confidence, 3),
                "latency_seconds": round(elapsed, 3),
            }

        except Exception as e:
            logger.error("Retrieval failed: %s", e)
            return {
                "results": [],
                "sources": [],
                "count": 0,
                "confidence": 0.0,
                "error": str(e),
                "latency_seconds": round(time.time() - start, 3),
            }


retrieval_service = RetrievalService()