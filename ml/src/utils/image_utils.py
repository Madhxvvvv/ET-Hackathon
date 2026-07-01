"""
image_utils.py
--------------
Low-level image helpers shared by the dataset pipeline and augmentation scripts.

All functions are pure (no global state) so they are trivially testable and
can be imported independently by future inference and training code.
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path

import cv2
import numpy as np

logger = logging.getLogger(__name__)


def is_valid_image(path: Path) -> bool:
    """
    Return True only if the file at *path* can be decoded as an image.

    Uses OpenCV to actually decode the file rather than just checking the
    extension, so corrupted or truncated files are caught here.
    """
    try:
        img = cv2.imread(str(path))
        return img is not None and img.size > 0
    except Exception:
        return False


def compute_file_hash(path: Path, chunk_size: int = 65_536) -> str:
    """
    Compute the SHA-256 hash of a file without loading it fully into RAM.

    Used by the dataset pipeline to detect exact duplicates regardless of
    filename.
    """
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while chunk := fh.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def resize_image(image: np.ndarray, size: tuple[int, int]) -> np.ndarray:
    """
    Resize an image to (height, width) using INTER_AREA for downscaling,
    INTER_CUBIC for upscaling.

    Args:
        image: HxWxC numpy array (BGR or RGB).
        size: (height, width) target dimensions.
    """
    h, w = size
    src_h, src_w = image.shape[:2]
    interpolation = cv2.INTER_AREA if (src_h > h or src_w > w) else cv2.INTER_CUBIC
    return cv2.resize(image, (w, h), interpolation=interpolation)


def load_image_bgr(path: Path) -> np.ndarray:
    """
    Load an image as a BGR numpy array. Raises FileNotFoundError if the
    file cannot be decoded.
    """
    img = cv2.imread(str(path))
    if img is None:
        raise FileNotFoundError(f"Cannot decode image: {path}")
    return img


def save_image(image: np.ndarray, dest: Path) -> None:
    """
    Write *image* to *dest*, creating parent directories as needed.

    Args:
        image: HxWxC numpy array.
        dest: Absolute path including filename and extension.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    success = cv2.imwrite(str(dest), image)
    if not success:
        raise OSError(f"cv2.imwrite failed for {dest}")


def collect_image_paths(
    directory: Path,
    extensions: frozenset[str],
    recursive: bool = False,
) -> list[Path]:
    """
    Return a sorted list of image paths in *directory* matching *extensions*.

    Args:
        directory: Root folder to search.
        extensions: Set of lowercase extensions including the dot, e.g. {'.jpg'}.
        recursive: When True, descend into sub-directories.
    """
    if not directory.exists():
        logger.warning("Directory does not exist: %s", directory)
        return []

    pattern = "**/*" if recursive else "*"
    paths = [
        p
        for p in directory.glob(pattern)
        if p.is_file() and p.suffix.lower() in extensions
    ]
    paths.sort()
    logger.debug("Found %d image(s) in %s (recursive=%s)", len(paths), directory, recursive)
    return paths
