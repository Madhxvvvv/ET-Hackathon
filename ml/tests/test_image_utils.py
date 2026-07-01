"""Tests for src/utils/image_utils.py."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
import pytest

from src.utils.image_utils import (
    collect_image_paths,
    compute_file_hash,
    is_valid_image,
    load_image_bgr,
    resize_image,
    save_image,
)
from configs.dataset_config import SUPPORTED_EXTENSIONS


class TestIsValidImage:
    def test_valid_jpeg_returns_true(self, valid_jpeg: Path):
        assert is_valid_image(valid_jpeg) is True

    def test_valid_png_returns_true(self, valid_png: Path):
        assert is_valid_image(valid_png) is True

    def test_corrupted_file_returns_false(self, corrupted_image: Path):
        assert is_valid_image(corrupted_image) is False

    def test_empty_file_returns_false(self, empty_file: Path):
        assert is_valid_image(empty_file) is False

    def test_nonexistent_file_returns_false(self, tmp_path: Path):
        assert is_valid_image(tmp_path / "ghost.jpg") is False


class TestComputeFileHash:
    def test_same_content_same_hash(self, valid_jpeg: Path, tmp_path: Path):
        copy = tmp_path / "copy.jpg"
        copy.write_bytes(valid_jpeg.read_bytes())
        assert compute_file_hash(valid_jpeg) == compute_file_hash(copy)

    def test_different_content_different_hash(self, valid_jpeg: Path, valid_png: Path):
        assert compute_file_hash(valid_jpeg) != compute_file_hash(valid_png)

    def test_hash_is_64_hex_chars(self, valid_jpeg: Path):
        h = compute_file_hash(valid_jpeg)
        assert len(h) == 64
        assert all(c in "0123456789abcdef" for c in h)


class TestResizeImage:
    def test_output_shape_matches_target(self):
        img = np.zeros((300, 400, 3), dtype=np.uint8)
        result = resize_image(img, (224, 224))
        assert result.shape == (224, 224, 3)

    def test_upscale_works(self):
        small = np.zeros((50, 50, 3), dtype=np.uint8)
        result = resize_image(small, (224, 224))
        assert result.shape == (224, 224, 3)


class TestLoadImageBgr:
    def test_returns_numpy_array(self, valid_jpeg: Path):
        img = load_image_bgr(valid_jpeg)
        assert isinstance(img, np.ndarray)
        assert img.ndim == 3

    def test_raises_for_nonexistent(self, tmp_path: Path):
        with pytest.raises(FileNotFoundError):
            load_image_bgr(tmp_path / "nope.jpg")

    def test_raises_for_corrupted(self, corrupted_image: Path):
        with pytest.raises(FileNotFoundError):
            load_image_bgr(corrupted_image)


class TestSaveImage:
    def test_saved_file_is_readable(self, tmp_path: Path):
        img = np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)
        dest = tmp_path / "sub" / "out.jpg"
        save_image(img, dest)
        assert dest.exists()
        reloaded = cv2.imread(str(dest))
        assert reloaded is not None

    def test_creates_parent_directories(self, tmp_path: Path):
        img = np.zeros((32, 32, 3), dtype=np.uint8)
        dest = tmp_path / "a" / "b" / "c" / "img.png"
        save_image(img, dest)
        assert dest.exists()


class TestCollectImagePaths:
    def test_finds_supported_extensions(self, tmp_image_dir: Path, valid_jpeg: Path, valid_png: Path):
        paths = collect_image_paths(tmp_image_dir, SUPPORTED_EXTENSIONS, recursive=True)
        names = {p.name for p in paths}
        assert valid_jpeg.name in names
        assert valid_png.name in names

    def test_ignores_unsupported_extensions(self, tmp_image_dir: Path, unsupported_format: Path):
        paths = collect_image_paths(tmp_image_dir, SUPPORTED_EXTENSIONS, recursive=True)
        assert unsupported_format not in paths

    def test_returns_empty_for_nonexistent_dir(self, tmp_path: Path):
        paths = collect_image_paths(tmp_path / "no_such_dir", SUPPORTED_EXTENSIONS)
        assert paths == []

    def test_non_recursive_does_not_descend(self, tmp_image_dir: Path, valid_jpeg: Path):
        # valid_jpeg is inside genuine/ sub-folder; non-recursive search from
        # tmp_image_dir should NOT find it.
        paths = collect_image_paths(tmp_image_dir, SUPPORTED_EXTENSIONS, recursive=False)
        assert valid_jpeg not in paths

    def test_results_are_sorted(self, tmp_image_dir: Path):
        for i in range(5):
            img = np.zeros((32, 32, 3), dtype=np.uint8)
            cv2.imwrite(str(tmp_image_dir / "genuine" / f"note_{i:03d}.jpg"), img)
        paths = collect_image_paths(tmp_image_dir, SUPPORTED_EXTENSIONS, recursive=True)
        assert paths == sorted(paths)
