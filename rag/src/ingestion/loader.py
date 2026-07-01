"""
loader.py
Loads raw documents (PDF / TXT / Markdown) into a normalized in-memory
representation before they're chunked and embedded.

Adding a new file type later = add one branch to `_load_single_file`.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from configs.config import get_logger

logger = get_logger(__name__)


@dataclass
class RawDocument:
    """Normalized representation of any loaded document, regardless of source type."""

    source_path: str
    content: str
    doc_type: str  # "pdf" | "txt" | "md"
    metadata: dict


class UnsupportedFileTypeError(Exception):
    pass


class EmptyDocumentError(Exception):
    pass


def _load_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as e:
        raise ImportError(
            "pypdf is required to load PDF files. Install with: pip install pypdf"
        ) from e

    reader = PdfReader(str(path))
    text_parts = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(text_parts).strip()


def _load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore").strip()


def _load_single_file(path: Path) -> RawDocument:
    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")

    suffix = path.suffix.lower()

    if suffix == ".pdf":
        content = _load_pdf(path)
        doc_type = "pdf"
    elif suffix in (".txt",):
        content = _load_text(path)
        doc_type = "txt"
    elif suffix in (".md", ".markdown"):
        content = _load_text(path)
        doc_type = "md"
    else:
        raise UnsupportedFileTypeError(
            f"Unsupported file type '{suffix}' for {path}. "
            f"Supported: .pdf, .txt, .md"
        )

    if not content or not content.strip():
        raise EmptyDocumentError(f"Document is empty after extraction: {path}")

    return RawDocument(
        source_path=str(path),
        content=content,
        doc_type=doc_type,
        metadata={
            "filename": path.name,
            "size_bytes": path.stat().st_size,
        },
    )


def load_documents(directory: Path, recursive: bool = True) -> list[RawDocument]:
    """
    Load every supported document under `directory`.
    Skips unsupported file types with a warning instead of crashing the whole batch.
    Skips empty/corrupt files with a warning, logs and continues.
    """
    directory = Path(directory)
    if not directory.exists():
        raise FileNotFoundError(f"Documents directory does not exist: {directory}")

    pattern = "**/*" if recursive else "*"
    candidate_files = [p for p in directory.glob(pattern) if p.is_file()]

    documents: list[RawDocument] = []
    seen_filenames: set[str] = set()

    for path in candidate_files:
        if path.suffix.lower() not in (".pdf", ".txt", ".md", ".markdown"):
            continue

        if path.name in seen_filenames:
            logger.warning("Duplicate document name skipped: %s", path.name)
            continue

        try:
            doc = _load_single_file(path)
            documents.append(doc)
            seen_filenames.add(path.name)
            logger.info("Loaded document: %s (%s)", path.name, doc.doc_type)
        except EmptyDocumentError as e:
            logger.warning("Skipping empty document: %s", e)
        except UnsupportedFileTypeError as e:
            logger.warning("Skipping unsupported file: %s", e)
        except Exception as e:  # noqa: BLE001 — log and continue batch ingestion
            logger.error("Failed to load %s: %s", path, e)

    logger.info("Loaded %d documents from %s", len(documents), directory)
    return documents
