"""
embeddings.py
Thin, swappable wrapper around an embedding model so the rest of the
codebase (ingest.py, retriever.py) never imports a specific provider's
SDK directly. Switching providers later = change RAG_EMBEDDING_PROVIDER
in .env, nothing else.

Day 1 default: sentence-transformers (local, free, no API key needed),
so the whole team can run ingestion without waiting on credentials.
"""

from __future__ import annotations

from functools import lru_cache

from configs.config import EMBEDDING_MODEL_NAME, EMBEDDING_PROVIDER, get_logger

logger = get_logger(__name__)


class EmbeddingProviderError(Exception):
    pass


@lru_cache(maxsize=1)
def get_embedding_function():
    """
    Returns a LangChain-compatible embedding object
    (implements .embed_documents() and .embed_query()).
    Cached so the model is loaded into memory once per process.
    """
    provider = EMBEDDING_PROVIDER.lower()

    if provider == "sentence-transformers":
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
        except ImportError as e:
            raise EmbeddingProviderError(
                "langchain-huggingface + sentence-transformers required. "
                "Install with: pip install langchain-huggingface sentence-transformers"
            ) from e

        logger.info("Loading local embedding model: %s", EMBEDDING_MODEL_NAME)
        return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    if provider == "openai":
        try:
            from langchain_openai import OpenAIEmbeddings
        except ImportError as e:
            raise EmbeddingProviderError(
                "langchain-openai required. Install with: pip install langchain-openai"
            ) from e
        logger.info("Using OpenAI embeddings: %s", EMBEDDING_MODEL_NAME)
        return OpenAIEmbeddings(model=EMBEDDING_MODEL_NAME)

    if provider == "cohere":
        try:
            from langchain_cohere import CohereEmbeddings
        except ImportError as e:
            raise EmbeddingProviderError(
                "langchain-cohere required. Install with: pip install langchain-cohere"
            ) from e
        logger.info("Using Cohere embeddings: %s", EMBEDDING_MODEL_NAME)
        return CohereEmbeddings(model=EMBEDDING_MODEL_NAME)

    raise EmbeddingProviderError(
        f"Unknown RAG_EMBEDDING_PROVIDER='{provider}'. "
        f"Supported: sentence-transformers, openai, cohere"
    )


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Convenience helper used by tests / scripts to embed a batch of strings directly."""
    if not texts:
        return []
    embedder = get_embedding_function()
    return embedder.embed_documents(texts)
