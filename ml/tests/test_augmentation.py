"""Tests for scripts/augment.py."""

from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.augment import augment_image, build_augmentation_pipeline
from configs.dataset_config import IMAGE_SIZE


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _random_bgr(h: int = 64, w: int = 64) -> np.ndarray:
    return np.random.randint(0, 255, (h, w, 3), dtype=np.uint8)


def _write_image(path: Path, h: int = 64, w: int = 64) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), _random_bgr(h, w))
    return path


# ---------------------------------------------------------------------------
# build_augmentation_pipeline
# ---------------------------------------------------------------------------

class TestBuildAugmentationPipeline:
    def test_returns_compose_object(self):
        import albumentations as A

        pipeline = build_augmentation_pipeline((224, 224))
        assert isinstance(pipeline, A.Compose)

    def test_pipeline_produces_correct_output_shape(self):
        pipeline = build_augmentation_pipeline((224, 224))
        rgb = cv2.cvtColor(_random_bgr(300, 400), cv2.COLOR_BGR2RGB)
        result = pipeline(image=rgb)["image"]
        assert result.shape == (224, 224, 3)

    def test_custom_size_is_respected(self):
        pipeline = build_augmentation_pipeline((128, 128))
        rgb = cv2.cvtColor(_random_bgr(64, 64), cv2.COLOR_BGR2RGB)
        result = pipeline(image=rgb)["image"]
        assert result.shape == (128, 128, 3)


# ---------------------------------------------------------------------------
# augment_image
# ---------------------------------------------------------------------------

class TestAugmentImage:
    def test_returns_correct_count(self):
        pipeline = build_augmentation_pipeline(IMAGE_SIZE)
        image = _random_bgr(64, 64)
        results = augment_image(image, pipeline, count=5)
        assert len(results) == 5

    def test_each_output_is_numpy_array(self):
        pipeline = build_augmentation_pipeline(IMAGE_SIZE)
        image = _random_bgr(64, 64)
        results = augment_image(image, pipeline, count=3)
        for r in results:
            assert isinstance(r, np.ndarray)
            assert r.ndim == 3

    def test_output_shape_matches_pipeline_size(self):
        target = (224, 224)
        pipeline = build_augmentation_pipeline(target)
        image = _random_bgr(512, 512)
        results = augment_image(image, pipeline, count=2)
        h, w = target
        for r in results:
            assert r.shape == (h, w, 3), f"Expected {(h, w, 3)}, got {r.shape}"

    def test_zero_count_returns_empty_list(self):
        pipeline = build_augmentation_pipeline(IMAGE_SIZE)
        image = _random_bgr(64, 64)
        results = augment_image(image, pipeline, count=0)
        assert results == []

    def test_augmented_images_are_not_identical_to_source(self):
        """With random transforms the output should differ from the input most of the time."""
        pipeline = build_augmentation_pipeline(IMAGE_SIZE)
        image = _random_bgr(224, 224)
        results = augment_image(image, pipeline, count=10)
        resized_src = cv2.resize(image, (224, 224))
        # At least half of the outputs should differ from the source.
        different = sum(1 for r in results if not np.array_equal(r, resized_src))
        assert different >= 5, "Expected most augmented images to differ from source"


# ---------------------------------------------------------------------------
# run_augmentation (integration)
# ---------------------------------------------------------------------------

class TestRunAugmentation:
    def test_correct_file_count_is_written(self, tmp_path: Path):
        from scripts.augment import run_augmentation

        src = tmp_path / "raw" / "genuine"
        dst = tmp_path / "augmented"
        for i in range(3):
            _write_image(src / f"note_{i:02d}.jpg")

        count = run_augmentation(source_dir=src.parent, dest_dir=dst, count=5)
        assert count == 15  # 3 images × 5 augmentations

    def test_output_files_are_decodable(self, tmp_path: Path):
        from scripts.augment import run_augmentation

        src = tmp_path / "raw" / "genuine"
        dst = tmp_path / "augmented"
        _write_image(src / "note_00.jpg")

        run_augmentation(source_dir=src.parent, dest_dir=dst, count=3)
        for p in dst.rglob("*.jpg"):
            img = cv2.imread(str(p))
            assert img is not None, f"Output image not readable: {p}"

    def test_raises_when_source_is_empty(self, tmp_path: Path):
        from scripts.augment import run_augmentation

        with pytest.raises(FileNotFoundError):
            run_augmentation(source_dir=tmp_path / "empty", dest_dir=tmp_path / "out", count=5)

    def test_class_subfolder_is_preserved(self, tmp_path: Path):
        from scripts.augment import run_augmentation

        src = tmp_path / "raw"
        (src / "genuine").mkdir(parents=True)
        (src / "counterfeit").mkdir(parents=True)
        _write_image(src / "genuine" / "g.jpg")
        _write_image(src / "counterfeit" / "c.jpg")

        dst = tmp_path / "aug"
        run_augmentation(source_dir=src, dest_dir=dst, count=2)

        assert (dst / "genuine").exists()
        assert (dst / "counterfeit").exists()
