"""
ingest.py
End-to-end ingestion pipeline:
  raw documents -> chunk -> embed -> persist to ChromaDB

Run directly via: python -m src.ingestion.ingest
or imported and called as `run_ingestion()` by scripts/ or future API routes.
"""

from __future__ import annotations

from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document

from configs.config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    COLLECTION_NAME,
    RAW_DOCS_DIR,
    VECTORDB_DIR,
    get_logger,
)
from src.ingestion.loader import RawDocument, load_documents
from src.utils.embeddings import get_embedding_function

logger = get_logger(__name__)


def chunk_documents(raw_documents: list[RawDocument]) -> list[Document]:
    """Split each raw document into overlapping chunks, preserving source metadata."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks: list[Document] = []
    for raw_doc in raw_documents:
        split_texts = splitter.split_text(raw_doc.content)
        for i, text in enumerate(split_texts):
            chunks.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": raw_doc.metadata["filename"],
                        "source_path": raw_doc.source_path,
                        "doc_type": raw_doc.doc_type,
                        "chunk_index": i,
                    },
                )
            )

    logger.info(
        "Chunked %d documents into %d chunks (size=%d, overlap=%d)",
        len(raw_documents),
        len(chunks),
        CHUNK_SIZE,
        CHUNK_OVERLAP,
    )
    return chunks


def build_vectorstore(chunks: list[Document], persist_dir: Path = VECTORDB_DIR) -> Chroma:
    """Embed chunks and persist them to a ChromaDB collection on disk."""
    if not chunks:
        raise ValueError("No chunks provided — cannot build an empty vector store.")

    embedding_fn = get_embedding_function()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_fn,
        collection_name=COLLECTION_NAME,
        persist_directory=str(persist_dir),
    )
    logger.info(
        "Persisted %d chunks to ChromaDB collection '%s' at %s",
        len(chunks),
        COLLECTION_NAME,
        persist_dir,
    )
    return vectorstore


def run_ingestion(raw_docs_dir: Path = RAW_DOCS_DIR) -> Chroma:
    """Full pipeline: load -> chunk -> embed -> persist. Returns the vectorstore handle."""
    logger.info("Starting ingestion run from %s", raw_docs_dir)
    raw_documents = load_documents(raw_docs_dir)

    if not raw_documents:
        raise RuntimeError(
            f"No valid documents found in {raw_docs_dir}. "
            f"Add .pdf/.txt/.md files before running ingestion."
        )

    chunks = chunk_documents(raw_documents)
    vectorstore = build_vectorstore(chunks)
    logger.info("Ingestion complete.")
    return vectorstore


if __name__ == "__main__":
    run_ingestion()
