"""
conftest.py
-----------
Shared pytest fixtures for the ML module test suite.
"""

from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np
import pytest

# Ensure ``ml/`` is on sys.path regardless of invocation directory.
ML_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ML_ROOT))


# ---------------------------------------------------------------------------
# Filesystem fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def tmp_image_dir(tmp_path: Path) -> Path:
    """Return a temporary directory pre-populated with one genuine and one counterfeit folder."""
    (tmp_path / "genuine").mkdir()
    (tmp_path / "counterfeit").mkdir()
    return tmp_path


@pytest.fixture()
def valid_jpeg(tmp_image_dir: Path) -> Path:
    """Write a valid 64×64 JPEG into genuine/ and return its path."""
    img = np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)
    path = tmp_image_dir / "genuine" / "note_001.jpg"
    cv2.imwrite(str(path), img)
    return path


@pytest.fixture()
def valid_png(tmp_image_dir: Path) -> Path:
    """Write a valid 128×128 PNG into counterfeit/ and return its path."""
    img = np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8)
    path = tmp_image_dir / "counterfeit" / "note_002.png"
    cv2.imwrite(str(path), img)
    return path


@pytest.fixture()
def corrupted_image(tmp_image_dir: Path) -> Path:
    """Write a file with a .jpg extension but garbage binary content."""
    path = tmp_image_dir / "genuine" / "corrupted.jpg"
    path.write_bytes(b"\x00\x01\x02\x03NOTANIMAGE")
    return path


@pytest.fixture()
def empty_file(tmp_image_dir: Path) -> Path:
    """Write a zero-byte file with a .jpg extension."""
    path = tmp_image_dir / "genuine" / "empty.jpg"
    path.write_bytes(b"")
    return path


@pytest.fixture()
def unsupported_format(tmp_image_dir: Path) -> Path:
    """Write a file with an unsupported extension (.webp)."""
    path = tmp_image_dir / "genuine" / "note.webp"
    img = np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)
    cv2.imwrite(str(path), img)
    return path
