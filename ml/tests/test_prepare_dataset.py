"""Tests for scripts/prepare_dataset.py."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import cv2
import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.prepare_dataset import (
    PrepareReport,
    SplitResult,
    copy_split,
    deduplicate,
    split_dataset,
    validate_images,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_image(path: Path, size: tuple[int, int] = (64, 64)) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    img = np.random.randint(0, 255, (*size, 3), dtype=np.uint8)
    cv2.imwrite(str(path), img)
    return path


def _make_images(base: Path, count: int, prefix: str = "img") -> list[Path]:
    paths = []
    for i in range(count):
        p = _write_image(base / f"{prefix}_{i:03d}.jpg")
        paths.append(p)
    return paths


# ---------------------------------------------------------------------------
# validate_images
# ---------------------------------------------------------------------------

class TestValidateImages:
    def test_valid_images_pass(self, tmp_path: Path):
        paths = _make_images(tmp_path, 5)
        valid, invalid = validate_images(paths)
        assert len(valid) == 5
        assert len(invalid) == 0

    def test_corrupted_image_is_invalid(self, corrupted_image: Path, valid_jpeg: Path):
        valid, invalid = validate_images([valid_jpeg, corrupted_image])
        assert valid_jpeg in valid
        assert corrupted_image in invalid

    def test_empty_file_is_invalid(self, empty_file: Path):
        _, invalid = validate_images([empty_file])
        assert empty_file in invalid

    def test_empty_input_returns_empty_lists(self):
        valid, invalid = validate_images([])
        assert valid == []
        assert invalid == []


# ---------------------------------------------------------------------------
# deduplicate
# ---------------------------------------------------------------------------

class TestDeduplicate:
    def test_no_duplicates(self, tmp_path: Path):
        paths = _make_images(tmp_path, 4)
        unique, dupes = deduplicate(paths)
        assert len(unique) == 4
        assert len(dupes) == 0

    def test_exact_duplicate_detected(self, tmp_path: Path):
        src = _write_image(tmp_path / "original.jpg")
        dup = tmp_path / "duplicate.jpg"
        shutil.copy2(src, dup)

        unique, dupes = deduplicate([src, dup])
        assert len(unique) == 1
        assert len(dupes) == 1
        assert src in unique
        assert dup in dupes

    def test_empty_input(self):
        unique, dupes = deduplicate([])
        assert unique == []
        assert dupes == []


# ---------------------------------------------------------------------------
# split_dataset
# ---------------------------------------------------------------------------

class TestSplitDataset:
    def test_correct_counts_for_clean_split(self, tmp_path: Path):
        paths = _make_images(tmp_path, 10)
        result = split_dataset(paths, train_ratio=0.7, val_ratio=0.15, seed=42)
        assert result.total == 10
        assert len(result.train) == 7
        assert len(result.val) == 2
        assert len(result.test) == 1

    def test_no_data_loss(self, tmp_path: Path):
        paths = _make_images(tmp_path, 13)  # Indivisible count.
        result = split_dataset(paths, train_ratio=0.7, val_ratio=0.15, seed=42)
        assert result.total == 13

    def test_reproducible_with_same_seed(self, tmp_path: Path):
        paths = _make_images(tmp_path, 20)
        r1 = split_dataset(paths, 0.7, 0.15, seed=99)
        r2 = split_dataset(paths, 0.7, 0.15, seed=99)
        assert r1.train == r2.train
        assert r1.val == r2.val
        assert r1.test == r2.test

    def test_different_seeds_produce_different_splits(self, tmp_path: Path):
        paths = _make_images(tmp_path, 20)
        r1 = split_dataset(paths, 0.7, 0.15, seed=1)
        r2 = split_dataset(paths, 0.7, 0.15, seed=2)
        assert r1.train != r2.train

    def test_empty_dataset_returns_empty_split(self):
        result = split_dataset([], 0.7, 0.15, seed=42)
        assert result.total == 0

    def test_single_image_goes_to_train(self, tmp_path: Path):
        paths = _make_images(tmp_path, 1)
        result = split_dataset(paths, 0.7, 0.15, seed=42)
        assert len(result.train) == 1

    def test_no_image_appears_in_multiple_splits(self, tmp_path: Path):
        paths = _make_images(tmp_path, 30)
        result = split_dataset(paths, 0.7, 0.15, seed=42)
        all_assigned = result.train + result.val + result.test
        assert len(all_assigned) == len(set(all_assigned)), "Duplicate assignment across splits"


# ---------------------------------------------------------------------------
# copy_split
# ---------------------------------------------------------------------------

class TestCopySplit:
    def test_files_are_copied_to_correct_dirs(self, tmp_path: Path):
        src = tmp_path / "raw" / "genuine"
        train_dir = tmp_path / "train"
        val_dir = tmp_path / "val"
        test_dir = tmp_path / "test"

        paths = _make_images(src, 6)
        split = SplitResult(train=paths[:4], val=paths[4:5], test=paths[5:])

        copy_split(split, train_dir, val_dir, test_dir)

        # Sub-folder (genuine/) should be preserved inside each split dir.
        assert any((train_dir / "genuine").iterdir())
        assert any((val_dir / "genuine").iterdir())
        assert any((test_dir / "genuine").iterdir())

    def test_destination_dirs_are_created(self, tmp_path: Path):
        src = tmp_path / "raw" / "genuine"
        train_dir = tmp_path / "brand_new" / "train"
        val_dir = tmp_path / "brand_new" / "val"
        test_dir = tmp_path / "brand_new" / "test"

        paths = _make_images(src, 3)
        split = SplitResult(train=paths[:2], val=paths[2:], test=[])
        copy_split(split, train_dir, val_dir, test_dir)

        assert train_dir.exists()
        assert val_dir.exists()

    def test_empty_split_does_not_raise(self, tmp_path: Path):
        split = SplitResult(train=[], val=[], test=[])
        copy_split(split, tmp_path / "t", tmp_path / "v", tmp_path / "te")
        # No error expected.

    def test_correct_file_count_in_each_split(self, tmp_path: Path):
        src = tmp_path / "raw" / "genuine"
        paths = _make_images(src, 10)
        split = SplitResult(train=paths[:7], val=paths[7:9], test=paths[9:])

        train_dir, val_dir, test_dir = tmp_path / "tr", tmp_path / "va", tmp_path / "te"
        copy_split(split, train_dir, val_dir, test_dir)

        def count_files(d: Path) -> int:
            return sum(1 for _ in d.rglob("*") if _.is_file())

        assert count_files(train_dir) == 7
        assert count_files(val_dir) == 2
        assert count_files(test_dir) == 1
