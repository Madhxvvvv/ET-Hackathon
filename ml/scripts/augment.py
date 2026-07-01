"""
augment.py
----------
Image augmentation pipeline for the Counterfeit Currency Detection module.

Design intent
~~~~~~~~~~~~~
~30 manually photographed currency notes need to expand to ~500+ training
images. This script applies a configurable Albumentations pipeline to every
image in ``datasets/raw_images/`` and writes the results to
``datasets/augmented/``.

Each augmentation is randomised independently per call, so running the
script N times per source image yields N statistically distinct outputs.

Usage
~~~~~
    python -m scripts.augment
    python -m scripts.augment --source datasets/raw_images --count 17
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import albumentations as A
import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from configs.dataset_config import (
    AUGMENTATIONS_PER_IMAGE,
    RAW_IMAGES_DIR,
    AUGMENTED_DIR,
    SUPPORTED_EXTENSIONS,
    DatasetConfig,
    load_config,
)
from src.utils import collect_image_paths, get_logger, load_image_bgr, save_image

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# Augmentation pipeline
# ---------------------------------------------------------------------------

def build_augmentation_pipeline(image_size: tuple[int, int]) -> A.Compose:
    """
    Return a randomised Albumentations pipeline suitable for currency note images.

    Augmentations are chosen to simulate realistic capture conditions:
    desk lighting variation, hand-held camera wobble, scanner compression,
    and slight physical deformation from handling.

    Args:
        image_size: (height, width) — output images are resized to this after aug.
    """
    h, w = image_size
    return A.Compose(
        [
            # ── Geometric distortions ─────────────────────────────────────
            A.Rotate(limit=15, border_mode=cv2.BORDER_REFLECT_101, p=0.8),
            A.Perspective(scale=(0.02, 0.06), p=0.5),           # camera angle shift
            A.Affine(
                translate_percent={"x": (-0.04, 0.04), "y": (-0.04, 0.04)},
                scale=(0.9, 1.15),                              # zoom in/out
                rotate=0,
                p=0.5,
            ),
            A.RandomResizedCrop(
                size=(h, w),
                scale=(0.85, 1.0),
                ratio=(0.9, 1.1),
                p=0.4,
            ),                                                   # small crops

            # ── Photometric / colour ──────────────────────────────────────
            A.RandomBrightnessContrast(
                brightness_limit=0.25,
                contrast_limit=0.25,
                p=0.8,
            ),
            A.HueSaturationValue(
                hue_shift_limit=8,
                sat_shift_limit=20,
                val_shift_limit=15,
                p=0.5,
            ),                                                   # colour variation
            A.RandomShadow(
                shadow_roi=(0, 0, 1, 1),
                num_shadows_limit=(1, 2),
                shadow_dimension=5,
                p=0.4,
            ),
            A.RandomToneCurve(scale=0.1, p=0.3),

            # ── Blur / noise ──────────────────────────────────────────────
            A.GaussNoise(std_range=(0.02, 0.11), p=0.5),
            A.MotionBlur(blur_limit=(3, 7), p=0.3),
            A.GaussianBlur(blur_limit=(3, 5), p=0.2),

            # ── Compression artefacts ─────────────────────────────────────
            A.ImageCompression(quality_range=(60, 95), p=0.4),

            # ── Physical deformation ──────────────────────────────────────
            A.ElasticTransform(
                alpha=30,
                sigma=6,
                border_mode=cv2.BORDER_REFLECT_101,
                p=0.25,
            ),                                                   # slight fold simulation
            A.GridDistortion(num_steps=4, distort_limit=0.1, p=0.2),

            # ── Resize to canonical shape last ────────────────────────────
            A.Resize(height=h, width=w),
        ]
    )


# ---------------------------------------------------------------------------
# Core function
# ---------------------------------------------------------------------------

def augment_image(
    image: np.ndarray,
    pipeline: A.Compose,
    count: int,
) -> list[np.ndarray]:
    """
    Apply *pipeline* to *image* independently *count* times.

    Args:
        image: BGR numpy array.
        pipeline: Compiled Albumentations Compose pipeline.
        count: Number of augmented variants to produce.

    Returns:
        List of *count* BGR numpy arrays.
    """
    results: list[np.ndarray] = []
    # Albumentations works in RGB.
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    for _ in range(count):
        augmented = pipeline(image=rgb)["image"]
        results.append(cv2.cvtColor(augmented, cv2.COLOR_RGB2BGR))
    return results


def run_augmentation(
    source_dir: Path | None = None,
    dest_dir: Path | None = None,
    count: int = AUGMENTATIONS_PER_IMAGE,
) -> int:
    """
    Full augmentation pass: load → augment → save.

    Preserves the ``genuine/`` / ``counterfeit/`` sub-folder structure so
    the augmented dataset is a drop-in replacement for the raw dataset.

    Args:
        source_dir: Root of source images. Defaults to ``raw_images/``.
        dest_dir: Root of augmented output. Defaults to ``augmented/``.
        count: Number of augmented images to generate per source file.

    Returns:
        Total number of augmented images written to disk.
    """
    cfg = load_config()
    src = source_dir or cfg.raw_images_dir
    dst = dest_dir or cfg.augmented_dir
    pipeline = build_augmentation_pipeline(cfg.image_size)

    image_paths = collect_image_paths(src, cfg.supported_extensions, recursive=True)
    if not image_paths:
        logger.error("No images found in %s. Add raw images before augmenting.", src)
        raise FileNotFoundError(f"No images in {src}")

    logger.info(
        "=== Augmentation Started === source=%s | images=%d | per_image=%d | expected_output≈%d",
        src, len(image_paths), count, len(image_paths) * count,
    )

    total_written = 0
    for src_path in image_paths:
        try:
            image = load_image_bgr(src_path)
        except FileNotFoundError:
            logger.warning("Skipping unreadable file: %s", src_path)
            continue

        augmented_images = augment_image(image, pipeline, count)

        # Mirror sub-folder structure (e.g. genuine/ or counterfeit/).
        class_folder = src_path.parent.name
        stem = src_path.stem

        for idx, aug_img in enumerate(augmented_images):
            dest_path = dst / class_folder / f"{stem}_aug{idx:03d}{src_path.suffix}"
            save_image(aug_img, dest_path)
            total_written += 1

        logger.debug("Augmented %s → %d files", src_path.name, count)

    logger.info(
        "=== Augmentation Complete === total written: %d images to %s",
        total_written, dst,
    )
    return total_written


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Augment currency note images.")
    parser.add_argument("--source", type=Path, default=None, help="Source directory (raw_images).")
    parser.add_argument("--dest", type=Path, default=None, help="Destination directory (augmented).")
    parser.add_argument(
        "--count",
        type=int,
        default=AUGMENTATIONS_PER_IMAGE,
        help=f"Augmentations per image (default: {AUGMENTATIONS_PER_IMAGE}).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    run_augmentation(source_dir=args.source, dest_dir=args.dest, count=args.count)
