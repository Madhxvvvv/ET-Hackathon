"""
logging_utils.py
----------------
Centralised logger factory for the ML module.

Every module that needs a logger calls get_logger(__name__). The first call
configures the root handler (console + rotating file); subsequent calls are
cheap because handlers are registered only once.
"""

from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

_CONFIGURED = False
_LOG_LEVEL = os.getenv("ML_LOG_LEVEL", "INFO").upper()
_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _configure_root(log_dir: Path) -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return

    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "ml.log"

    fmt = logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT)

    console = logging.StreamHandler()
    console.setFormatter(fmt)

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(fmt)

    root = logging.getLogger()
    root.setLevel(_LOG_LEVEL)
    root.addHandler(console)
    root.addHandler(file_handler)

    _CONFIGURED = True


def get_logger(name: str, log_dir: Path | None = None) -> logging.Logger:
    """
    Return a named logger. Configures root logger on first call.

    Args:
        name: Typically ``__name__`` of the calling module.
        log_dir: Directory for the log file. Defaults to ``ml/logs/``.
    """
    if log_dir is None:
        from configs.dataset_config import LOGS_DIR  # late import to avoid circularity

        log_dir = LOGS_DIR

    _configure_root(log_dir)
    return logging.getLogger(name)
