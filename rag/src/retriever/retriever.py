"""
retriever.py
Loads the persisted ChromaDB collection and exposes a stable retrieval
function. This is the contract Person 2 (backend) will eventually wrap
in a FastAPI route (`/scam-shield/query`), and Person 4's own Day 2
chatbot/agent will call internally — so the signature here should not
change without telling the rest of the team.
"""

from __future__ import annotations

from dataclasses import dataclass

from langchain_chroma import Chroma

from configs.config import COLLECTION_NAME, DEFAULT_TOP_K, VECTORDB_DIR, get_logger
from src.utils.embeddings import get_embedding_function

logger = get_logger(__name__)


@dataclass
class RetrievedChunk:
    content: str
    source: str
    score: float | None
    metadata: dict


class RetrieverNotInitializedError(Exception):
    pass


def _load_vectorstore() -> Chroma:
    embedding_fn = get_embedding_function()
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_fn,
        persist_directory=str(VECTORDB_DIR),
    )

    if vectorstore._collection.count() == 0:
        raise RetrieverNotInitializedError(
            "Vector store is empty. Run ingestion first: "
            "python -m src.ingestion.ingest"
        )
    return vectorstore


def retrieve(query: str, k: int = DEFAULT_TOP_K) -> list[RetrievedChunk]:
    """
    Stable public entrypoint. Returns top-k most relevant chunks for `query`.

    This is the function Person 2 / Person 3 should call (directly today,
    via an API wrapper later) — keep this signature stable across Day 2+.
    """
    if not query or not query.strip():
        raise ValueError("Query must be a non-empty string.")
    if k < 1:
        raise ValueError("k must be >= 1.")

    vectorstore = _load_vectorstore()
    results = vectorstore.similarity_search_with_score(query, k=k)

    retrieved = [
        RetrievedChunk(
            content=doc.page_content,
            source=doc.metadata.get("source", "unknown"),
            score=float(score),
            metadata=doc.metadata,
        )
        for doc, score in results
    ]
    logger.info("Retrieved %d chunks for query: %r", len(retrieved), query[:80])
    return retrieved


def retrieve_as_context_string(query: str, k: int = DEFAULT_TOP_K) -> str:
    """Convenience helper for Day 2 prompt assembly: joins chunks into one context block."""
    chunks = retrieve(query, k=k)
    return "\n\n---\n\n".join(
        f"[Source: {c.source}]\n{c.content}" for c in chunks
    )
