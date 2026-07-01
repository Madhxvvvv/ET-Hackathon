"""
dataset_config.py
-----------------
Central configuration for the Counterfeit Currency Detection ML module.

All hyper-parameters, paths, and dataset settings live here. Import from
this module rather than hardcoding values anywhere else. Override defaults
via environment variables (ML_* prefix) so the same code runs in dev, CI,
and production without file edits.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Module root — the ml/ directory, regardless of where the script is invoked.
# ---------------------------------------------------------------------------
MODULE_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Dataset paths
# ---------------------------------------------------------------------------
def _path(env_var: str, default: Path) -> Path:
    raw = os.getenv(env_var)
    return Path(raw) if raw else default


DATASETS_DIR = _path("ML_DATASETS_DIR", MODULE_ROOT / "datasets")
RAW_IMAGES_DIR = _path("ML_RAW_IMAGES_DIR", DATASETS_DIR / "raw_images")
AUGMENTED_DIR = _path("ML_AUGMENTED_DIR", DATASETS_DIR / "augmented")
TRAIN_DIR = _path("ML_TRAIN_DIR", DATASETS_DIR / "train")
VAL_DIR = _path("ML_VAL_DIR", DATASETS_DIR / "validation")
TEST_DIR = _path("ML_TEST_DIR", DATASETS_DIR / "test")
MODELS_DIR = _path("ML_MODELS_DIR", MODULE_ROOT / "models")
LOGS_DIR = _path("ML_LOGS_DIR", MODULE_ROOT / "logs")

# ---------------------------------------------------------------------------
# Image settings
# ---------------------------------------------------------------------------
IMAGE_SIZE: tuple[int, int] = (224, 224)  # (height, width) — EfficientNet default
SUPPORTED_EXTENSIONS: frozenset[str] = frozenset({".jpg", ".jpeg", ".png", ".bmp", ".tiff"})

# ---------------------------------------------------------------------------
# Dataset split ratios (must sum to 1.0)
# ---------------------------------------------------------------------------
TRAIN_RATIO: float = float(os.getenv("ML_TRAIN_RATIO", "0.70"))
VAL_RATIO: float = float(os.getenv("ML_VAL_RATIO", "0.15"))
TEST_RATIO: float = float(os.getenv("ML_TEST_RATIO", "0.15"))

# ---------------------------------------------------------------------------
# Augmentation
# ---------------------------------------------------------------------------
AUGMENTATIONS_PER_IMAGE: int = int(os.getenv("ML_AUGMENTATIONS_PER_IMAGE", "17"))
# 30 base images × 17 augmentations ≈ 510 augmented images

# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------
RANDOM_SEED: int = int(os.getenv("ML_RANDOM_SEED", "42"))

# ---------------------------------------------------------------------------
# Supported currency denominations (used for label validation)
# ---------------------------------------------------------------------------
SUPPORTED_DENOMINATIONS: tuple[str, ...] = (
    "10",
    "20",
    "50",
    "100",
    "200",
    "500",
    "2000",
)

# Class labels — 0 = genuine, 1 = counterfeit
CLASS_LABELS: dict[str, int] = {"genuine": 0, "counterfeit": 1}


def _validate_splits() -> None:
    total = round(TRAIN_RATIO + VAL_RATIO + TEST_RATIO, 6)
    if total != 1.0:
        raise ValueError(
            f"Split ratios must sum to 1.0, got {total} "
            f"(train={TRAIN_RATIO}, val={VAL_RATIO}, test={TEST_RATIO})."
        )


_validate_splits()


@dataclass(frozen=True)
class DatasetConfig:
    """Immutable snapshot of all dataset settings. Pass this around instead of globals."""

    # Paths
    raw_images_dir: Path = RAW_IMAGES_DIR
    augmented_dir: Path = AUGMENTED_DIR
    train_dir: Path = TRAIN_DIR
    val_dir: Path = VAL_DIR
    test_dir: Path = TEST_DIR
    models_dir: Path = MODELS_DIR
    logs_dir: Path = LOGS_DIR

    # Image
    image_size: tuple[int, int] = IMAGE_SIZE
    supported_extensions: frozenset[str] = field(default_factory=lambda: SUPPORTED_EXTENSIONS)

    # Splits
    train_ratio: float = TRAIN_RATIO
    val_ratio: float = VAL_RATIO
    test_ratio: float = TEST_RATIO

    # Augmentation
    augmentations_per_image: int = AUGMENTATIONS_PER_IMAGE

    # Misc
    random_seed: int = RANDOM_SEED
    supported_denominations: tuple[str, ...] = SUPPORTED_DENOMINATIONS
    class_labels: dict[str, int] = field(default_factory=lambda: dict(CLASS_LABELS))

    def all_split_dirs(self) -> list[Path]:
        return [self.train_dir, self.val_dir, self.test_dir]


def load_config() -> DatasetConfig:
    """Return the active DatasetConfig, creating log/model dirs as a side-effect."""
    cfg = DatasetConfig()
    for d in (cfg.logs_dir, cfg.models_dir):
        d.mkdir(parents=True, exist_ok=True)
    logger.debug("DatasetConfig loaded: %s", cfg)
    return cfg
