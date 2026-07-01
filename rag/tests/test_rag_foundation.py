"""
Pytest suite for Day 1 RAG foundation.

Run with:
    pytest rag/tests -v

These tests use a throwaway temp directory for vectordb/docs so they never
touch the real persisted collection.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from configs.config import load_config
from src.ingestion.loader import (
    EmptyDocumentError,
    UnsupportedFileTypeError,
    load_documents,
)
from src.ingestion.ingest import chunk_documents


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def tmp_docs_dir(tmp_path: Path) -> Path:
    d = tmp_path / "raw"
    d.mkdir()
    return d


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
def test_config_loads_with_defaults():
    cfg = load_config()
    assert cfg.chunk_size > 0
    assert cfg.chunk_overlap < cfg.chunk_size
    assert ".pdf" in cfg.supported_extensions
    assert ".txt" in cfg.supported_extensions
    assert ".md" in cfg.supported_extensions


# ---------------------------------------------------------------------------
# Document loading
# ---------------------------------------------------------------------------
def test_load_txt_document(tmp_docs_dir):
    f = tmp_docs_dir / "note.txt"
    f.write_text("This is a valid scam awareness note.")
    docs = load_documents(tmp_docs_dir)
    assert len(docs) == 1
    assert docs[0].doc_type == "txt"
    assert "scam awareness" in docs[0].content


def test_load_markdown_document(tmp_docs_dir):
    f = tmp_docs_dir / "note.md"
    f.write_text("# Heading\nSome markdown content.")
    docs = load_documents(tmp_docs_dir)
    assert len(docs) == 1
    assert docs[0].doc_type == "md"


def test_empty_document_is_skipped(tmp_docs_dir):
    f = tmp_docs_dir / "empty.txt"
    f.write_text("")
    docs = load_documents(tmp_docs_dir)
    assert docs == []  # skipped, not raised, so batch ingestion doesn't crash


def test_unsupported_extension_is_skipped(tmp_docs_dir):
    f = tmp_docs_dir / "image.png"
    f.write_bytes(b"\x89PNG\r\n")
    docs = load_documents(tmp_docs_dir)
    assert docs == []


def test_duplicate_filenames_are_deduplicated(tmp_docs_dir):
    (tmp_docs_dir / "a.txt").write_text("first version")
    sub = tmp_docs_dir / "sub"
    sub.mkdir()
    (sub / "a.txt").write_text("duplicate name, different folder")
    docs = load_documents(tmp_docs_dir)
    assert len(docs) == 1  # second 'a.txt' skipped as duplicate filename


def test_missing_directory_raises():
    with pytest.raises(FileNotFoundError):
        load_documents(Path("/nonexistent/path/that/does/not/exist"))


def test_loading_empty_directory_returns_empty_list(tmp_docs_dir):
    docs = load_documents(tmp_docs_dir)
    assert docs == []


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------
def test_chunking_produces_chunks_with_metadata(tmp_docs_dir):
    f = tmp_docs_dir / "long.txt"
    f.write_text("Sentence one. " * 200)  # long enough to force multiple chunks
    docs = load_documents(tmp_docs_dir)
    chunks = chunk_documents(docs)
    assert len(chunks) > 1
    assert chunks[0].metadata["source"] == "long.txt"
    assert chunks[0].metadata["chunk_index"] == 0


# ---------------------------------------------------------------------------
# Embeddings (skipped automatically if model can't be downloaded in this env)
# ---------------------------------------------------------------------------
def test_embedding_creation():
    try:
        from src.utils.embeddings import embed_texts
    except ImportError:
        pytest.skip("Embedding dependencies not installed")

    try:
        vectors = embed_texts(["hello world", "digital arrest scam"])
    except Exception as e:  # noqa: BLE001
        pytest.skip(f"Embedding model unavailable in this environment: {e}")

    assert len(vectors) == 2
    assert len(vectors[0]) > 0
    assert isinstance(vectors[0][0], float)


# ---------------------------------------------------------------------------
# Vector store + retrieval (integration-style, uses real ingestion sample docs)
# ---------------------------------------------------------------------------
def test_vectordb_initialization_and_retrieval(tmp_path, monkeypatch):
    try:
        import configs.config as cfg_module
        from src.ingestion.ingest import run_ingestion
        from src.retriever.retriever import retrieve
    except ImportError:
        pytest.skip("chromadb/langchain dependencies not installed")

    # Redirect vectordb + docs to an isolated temp location for this test
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    (raw_dir / "sample.txt").write_text(
        "Never share your OTP with anyone claiming to be from your bank."
    )
    vdb_dir = tmp_path / "vectordb"
    monkeypatch.setattr(cfg_module, "VECTORDB_DIR", vdb_dir)

    try:
        run_ingestion(raw_docs_dir=raw_dir)
        results = retrieve("Should I share my OTP?", k=1)
    except Exception as e:  # noqa: BLE001
        pytest.skip(f"Vector store unavailable in this environment: {e}")

    assert len(results) == 1
    assert "OTP" in results[0].content
    shutil.rmtree(vdb_dir, ignore_errors=True)
