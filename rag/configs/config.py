"""
Central configuration for the Digital Arrest Scam Shield RAG module.

All paths, model names, and runtime parameters are pulled from environment
variables (with sane defaults) so the module behaves the same in dev,
CI, and whatever environment Person 2's backend deploys it in.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
MODULE_ROOT = Path(__file__).resolve().parent.parent  # rag/

RAW_DOCS_DIR = Path(os.getenv("RAG_RAW_DOCS_DIR", MODULE_ROOT / "documents" / "raw"))
PROCESSED_DOCS_DIR = Path(
    os.getenv("RAG_PROCESSED_DOCS_DIR", MODULE_ROOT / "documents" / "processed")
)
VECTORDB_DIR = Path(os.getenv("RAG_VECTORDB_DIR", MODULE_ROOT / "vectordb"))
LOG_DIR = Path(os.getenv("RAG_LOG_DIR", MODULE_ROOT / "logs"))

for d in (RAW_DOCS_DIR, PROCESSED_DOCS_DIR, VECTORDB_DIR, LOG_DIR):
    d.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Embedding / Vector DB config
# ---------------------------------------------------------------------------
EMBEDDING_PROVIDER = os.getenv("RAG_EMBEDDING_PROVIDER", "sentence-transformers")
# Default to a free local model so Day 1 works with zero API keys.
# Swap to "text-embedding-3-small" / Cohere etc. later by changing env var only.
EMBEDDING_MODEL_NAME = os.getenv(
    "RAG_EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2"
)
COLLECTION_NAME = os.getenv("RAG_COLLECTION_NAME", "scam_shield_knowledge_base")

# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------
CHUNK_SIZE = int(os.getenv("RAG_CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("RAG_CHUNK_OVERLAP", "120"))

# ---------------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------------
DEFAULT_TOP_K = int(os.getenv("RAG_DEFAULT_TOP_K", "4"))

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_LEVEL = os.getenv("RAG_LOG_LEVEL", "INFO")


def get_logger(name: str) -> logging.Logger:
    """Return a module-level logger that writes to console + rag/logs/rag.log."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # avoid duplicate handlers on re-import

    logger.setLevel(LOG_LEVEL)
    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(fmt)

    file_handler = logging.FileHandler(LOG_DIR / "rag.log")
    file_handler.setFormatter(fmt)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


@dataclass(frozen=True)
class RAGConfig:
    """Snapshot of config, useful to pass around / log / assert in tests."""

    raw_docs_dir: Path = RAW_DOCS_DIR
    processed_docs_dir: Path = PROCESSED_DOCS_DIR
    vectordb_dir: Path = VECTORDB_DIR
    embedding_provider: str = EMBEDDING_PROVIDER
    embedding_model_name: str = EMBEDDING_MODEL_NAME
    collection_name: str = COLLECTION_NAME
    chunk_size: int = CHUNK_SIZE
    chunk_overlap: int = CHUNK_OVERLAP
    default_top_k: int = DEFAULT_TOP_K
    supported_extensions: tuple[str, ...] = field(
        default_factory=lambda: (".pdf", ".txt", ".md")
    )


def load_config() -> RAGConfig:
    return RAGConfig()
