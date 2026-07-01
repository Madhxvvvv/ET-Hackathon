"""
prepare_dataset.py
------------------
Dataset preparation pipeline for the Counterfeit Currency Detection module.

Responsibilities
~~~~~~~~~~~~~~~~
- Validate every image file in ``raw_images/`` (extension check + decode check).
- Detect and report exact duplicates (SHA-256 hash comparison).
- Shuffle and split the valid image list into train / validation / test sets.
- Copy files into the appropriate split directories, preserving the
  ``genuine/`` vs ``counterfeit/`` sub-folder structure.
- Auto-create all destination directories.
- Write a JSON summary report of every run.

Usage
~~~~~
    python -m scripts.prepare_dataset
    python -m scripts.prepare_dataset --source datasets/raw_images --seed 7

The script is idempotent: re-running it will overwrite existing split files.
"""

from __future__ import annotations

import argparse
import json
import random
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

# Allow running as `python -m scripts.prepare_dataset` from ml/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from configs.dataset_config import (
    RANDOM_SEED,
    RAW_IMAGES_DIR,
    SUPPORTED_EXTENSIONS,
    TEST_RATIO,
    TRAIN_RATIO,
    VAL_RATIO,
    DatasetConfig,
    load_config,
)
from src.utils import collect_image_paths, compute_file_hash, get_logger, is_valid_image

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class SplitResult:
    train: list[Path]
    val: list[Path]
    test: list[Path]

    @property
    def total(self) -> int:
        return len(self.train) + len(self.val) + len(self.test)


@dataclass
class PrepareReport:
    source_dir: str
    total_found: int
    invalid_count: int
    duplicate_count: int
    prepared_count: int
    train_count: int
    val_count: int
    test_count: int
    invalid_files: list[str]
    duplicate_files: list[str]


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def validate_images(
    paths: list[Path],
) -> tuple[list[Path], list[Path]]:
    """
    Partition *paths* into (valid, invalid) by decoding each file with OpenCV.

    Returns:
        valid: Images that can be decoded.
        invalid: Files that cannot be decoded (corrupted, empty, wrong format).
    """
    valid: list[Path] = []
    invalid: list[Path] = []

    for p in paths:
        if is_valid_image(p):
            valid.append(p)
        else:
            logger.warning("Invalid/corrupted image skipped: %s", p.name)
            invalid.append(p)

    logger.info("Validation: %d valid, %d invalid out of %d files.", len(valid), len(invalid), len(paths))
    return valid, invalid


def deduplicate(paths: list[Path]) -> tuple[list[Path], list[Path]]:
    """
    Remove exact duplicates based on SHA-256 file hash.

    Returns:
        unique: First occurrence of each unique file.
        duplicates: All subsequent occurrences (omitted from the dataset).
    """
    seen: dict[str, Path] = {}
    unique: list[Path] = []
    duplicates: list[Path] = []

    for p in paths:
        file_hash = compute_file_hash(p)
        if file_hash in seen:
            logger.warning("Duplicate detected: %s is identical to %s", p.name, seen[file_hash].name)
            duplicates.append(p)
        else:
            seen[file_hash] = p
            unique.append(p)

    logger.info("Deduplication: %d unique, %d duplicates removed.", len(unique), len(duplicates))
    return unique, duplicates


def split_dataset(
    paths: list[Path],
    train_ratio: float,
    val_ratio: float,
    seed: int,
) -> SplitResult:
    """
    Randomly shuffle *paths* and split into train / val / test.

    The test split receives whatever remains after train and val are cut so
    that every image is assigned even when ``len(paths)`` is not perfectly
    divisible.
    """
    if not paths:
        return SplitResult(train=[], val=[], test=[])

    rng = random.Random(seed)
    shuffled = list(paths)
    rng.shuffle(shuffled)

    n = len(shuffled)
    n_train = max(1, round(n * train_ratio))
    n_val = max(0, round(n * val_ratio))
    # Test gets the remainder to avoid rounding-induced data loss.
    n_train = min(n_train, n)
    n_val = min(n_val, n - n_train)

    train = shuffled[:n_train]
    val = shuffled[n_train : n_train + n_val]
    test = shuffled[n_train + n_val :]

    logger.info(
        "Split: %d train | %d val | %d test (seed=%d, ratios=%.2f/%.2f/%.2f)",
        len(train), len(val), len(test), seed, train_ratio, val_ratio, 1 - train_ratio - val_ratio,
    )
    return SplitResult(train=train, val=val, test=test)


def copy_split(
    split: SplitResult,
    train_dir: Path,
    val_dir: Path,
    test_dir: Path,
) -> None:
    """
    Copy each file in the split to its destination directory.

    The sub-folder structure under ``raw_images/`` (e.g. ``genuine/`` /
    ``counterfeit/``) is preserved so that torchvision's ``ImageFolder``
    loader can infer class labels automatically.
    """
    mapping: list[tuple[list[Path], Path]] = [
        (split.train, train_dir),
        (split.val, val_dir),
        (split.test, test_dir),
    ]

    for paths, dest_root in mapping:
        dest_root.mkdir(parents=True, exist_ok=True)
        for src in paths:
            # Preserve the class sub-folder (genuine / counterfeit).
            dest = dest_root / src.parent.name / src.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)

    logger.info("Files copied: %d train, %d val, %d test.", len(split.train), len(split.val), len(split.test))


def write_report(report: PrepareReport, cfg: DatasetConfig) -> None:
    report_path = cfg.logs_dir / "prepare_dataset_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", encoding="utf-8") as fh:
        json.dump(asdict(report), fh, indent=2, default=str)
    logger.info("Report written to %s", report_path)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run_prepare(
    source_dir: Path | None = None,
    train_ratio: float = TRAIN_RATIO,
    val_ratio: float = VAL_RATIO,
    seed: int = RANDOM_SEED,
) -> PrepareReport:
    """
    Full pipeline: validate → deduplicate → split → copy → report.

    Args:
        source_dir: Override for ``raw_images/`` (defaults to config value).
        train_ratio: Fraction of data for training.
        val_ratio: Fraction of data for validation.
        seed: Random seed for reproducible shuffles.

    Returns:
        PrepareReport dataclass with counts and file lists.
    """
    cfg = load_config()
    src = source_dir or cfg.raw_images_dir

    logger.info("=== Dataset Preparation Started ===")
    logger.info("Source: %s", src)

    all_paths = collect_image_paths(src, cfg.supported_extensions, recursive=True)
    if not all_paths:
        logger.error("No images found in %s. Add images before running this script.", src)
        raise FileNotFoundError(f"No images found in {src}")

    logger.info("Found %d image file(s).", len(all_paths))

    valid, invalid = validate_images(all_paths)
    unique, duplicates = deduplicate(valid)
    split = split_dataset(unique, train_ratio, val_ratio, seed)
    copy_split(split, cfg.train_dir, cfg.val_dir, cfg.test_dir)

    report = PrepareReport(
        source_dir=str(src),
        total_found=len(all_paths),
        invalid_count=len(invalid),
        duplicate_count=len(duplicates),
        prepared_count=len(unique),
        train_count=len(split.train),
        val_count=len(split.val),
        test_count=len(split.test),
        invalid_files=[str(p) for p in invalid],
        duplicate_files=[str(p) for p in duplicates],
    )
    write_report(report, cfg)

    logger.info(
        "=== Dataset Preparation Complete === "
        "total=%d | invalid=%d | duplicates=%d | prepared=%d "
        "(train=%d / val=%d / test=%d)",
        report.total_found,
        report.invalid_count,
        report.duplicate_count,
        report.prepared_count,
        report.train_count,
        report.val_count,
        report.test_count,
    )
    return report


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare the currency detection dataset.")
    parser.add_argument("--source", type=Path, default=None, help="Path to raw_images directory.")
    parser.add_argument("--train-ratio", type=float, default=TRAIN_RATIO)
    parser.add_argument("--val-ratio", type=float, default=VAL_RATIO)
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    run_prepare(
        source_dir=args.source,
        train_ratio=args.train_ratio,
        val_ratio=args.val_ratio,
        seed=args.seed,
    )
