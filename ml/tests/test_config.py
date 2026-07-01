"""Tests for configs/dataset_config.py."""

from __future__ import annotations

import importlib
import os
from pathlib import Path

import pytest


class TestDatasetConfig:
    def test_load_config_returns_instance(self):
        from configs.dataset_config import DatasetConfig, load_config

        cfg = load_config()
        assert isinstance(cfg, DatasetConfig)

    def test_split_ratios_sum_to_one(self):
        from configs.dataset_config import TEST_RATIO, TRAIN_RATIO, VAL_RATIO

        total = round(TRAIN_RATIO + VAL_RATIO + TEST_RATIO, 6)
        assert total == 1.0, f"Split ratios sum to {total}, expected 1.0"

    def test_supported_extensions_are_lowercase(self):
        from configs.dataset_config import SUPPORTED_EXTENSIONS

        for ext in SUPPORTED_EXTENSIONS:
            assert ext == ext.lower(), f"Extension {ext!r} should be lowercase"
            assert ext.startswith("."), f"Extension {ext!r} should start with a dot"

    def test_image_size_positive(self):
        from configs.dataset_config import IMAGE_SIZE

        h, w = IMAGE_SIZE
        assert h > 0 and w > 0

    def test_augmentations_per_image_positive(self):
        from configs.dataset_config import AUGMENTATIONS_PER_IMAGE

        assert AUGMENTATIONS_PER_IMAGE >= 1

    def test_class_labels_contains_genuine_and_counterfeit(self):
        from configs.dataset_config import CLASS_LABELS

        assert "genuine" in CLASS_LABELS
        assert "counterfeit" in CLASS_LABELS
        # Values should be distinct integers.
        assert CLASS_LABELS["genuine"] != CLASS_LABELS["counterfeit"]

    def test_env_override_train_ratio(self, monkeypatch):
        """ML_TRAIN_RATIO env var should override the default."""
        monkeypatch.setenv("ML_TRAIN_RATIO", "0.80")
        monkeypatch.setenv("ML_VAL_RATIO", "0.10")
        monkeypatch.setenv("ML_TEST_RATIO", "0.10")

        import configs.dataset_config as cfg_mod

        importlib.reload(cfg_mod)

        assert cfg_mod.TRAIN_RATIO == pytest.approx(0.80)
        # Reset to avoid polluting other tests.
        importlib.reload(cfg_mod)

    def test_invalid_split_raises_on_import(self, monkeypatch):
        """Splits that don't sum to 1.0 should raise ValueError at module load."""
        monkeypatch.setenv("ML_TRAIN_RATIO", "0.50")
        monkeypatch.setenv("ML_VAL_RATIO", "0.50")
        monkeypatch.setenv("ML_TEST_RATIO", "0.50")  # sum = 1.50

        import configs.dataset_config as cfg_mod

        with pytest.raises(ValueError, match="sum to 1.0"):
            importlib.reload(cfg_mod)

        # Restore sane defaults.
        monkeypatch.delenv("ML_TRAIN_RATIO")
        monkeypatch.delenv("ML_VAL_RATIO")
        monkeypatch.delenv("ML_TEST_RATIO")
        importlib.reload(cfg_mod)

    def test_config_is_frozen(self):
        from configs.dataset_config import load_config

        cfg = load_config()
        with pytest.raises((AttributeError, TypeError)):
            cfg.train_ratio = 0.999  # type: ignore[misc]

    def test_logs_dir_created_by_load_config(self, tmp_path: Path, monkeypatch):
        monkeypatch.setenv("ML_LOGS_DIR", str(tmp_path / "new_logs"))
        import configs.dataset_config as cfg_mod

        importlib.reload(cfg_mod)
        cfg_mod.load_config()
        assert (tmp_path / "new_logs").exists()
        importlib.reload(cfg_mod)
