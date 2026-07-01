"""
language_detector.py
Detects language of user input.
Supports English, Hindi, and Hinglish detection.
"""

from __future__ import annotations

from configs.config import get_logger
from src.utils.language_config import (
    DEFAULT_LANGUAGE,
    HINDI_CHAR_THRESHOLD,
    HINDI_UNICODE_END,
    HINDI_UNICODE_START,
    HINGLISH_MARKERS,
)

logger = get_logger(__name__)


def _count_hindi_chars(text: str) -> int:
    return sum(1 for c in text if HINDI_UNICODE_START <= c <= HINDI_UNICODE_END)


def _count_hinglish_markers(text: str) -> int:
    lower = text.lower()
    return sum(1 for marker in HINGLISH_MARKERS if marker in lower)


def detect_language(text: str) -> str:
    """
    Detect language of input text.

    Returns:
        Language code: 'en', 'hi', or 'hinglish'
    """
    if not text or not text.strip():
        return DEFAULT_LANGUAGE

    hindi_chars = _count_hindi_chars(text)
    hinglish_count = _count_hinglish_markers(text)

    # Pure Hindi — has Devanagari script
    if hindi_chars > HINDI_CHAR_THRESHOLD:
        # Mixed script = Hinglish
        english_words = len([w for w in text.split() if w.isascii()])
        if english_words > 2:
            logger.debug("Detected: hinglish (mixed script)")
            return "hinglish"
        logger.debug("Detected: hindi")
        return "hi"

    # Hinglish — Roman script but Hindi words
    if hinglish_count >= 2:
        logger.debug("Detected: hinglish (roman hindi)")
        return "hinglish"

    # Fallback to langdetect
    try:
        from langdetect import detect
        lang = detect(text)
        logger.debug("langdetect result: %s", lang)
        if lang == "hi":
            return "hi"
        return "en"
    except Exception:
        return DEFAULT_LANGUAGE