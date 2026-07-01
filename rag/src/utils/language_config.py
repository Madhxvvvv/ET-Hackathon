"""
language_config.py
Language configuration for multilingual support.
Defines supported languages, codes, and display names.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LanguageConfig:
    code: str          # langdetect code
    display_name: str  # human readable
    native_name: str   # name in that language
    supported: bool    # fully supported today


SUPPORTED_LANGUAGES: dict[str, LanguageConfig] = {
    "en": LanguageConfig("en", "English", "English", True),
    "hi": LanguageConfig("hi", "Hindi", "हिंदी", True),
    "hinglish": LanguageConfig("hinglish", "Hinglish", "Hinglish", True),
    "ta": LanguageConfig("ta", "Tamil", "தமிழ்", False),
    "te": LanguageConfig("te", "Telugu", "తెలుగు", False),
    "mr": LanguageConfig("mr", "Marathi", "मराठी", False),
    "gu": LanguageConfig("gu", "Gujarati", "ગુજરાતી", False),
    "pa": LanguageConfig("pa", "Punjabi", "ਪੰਜਾਬੀ", False),
    "bn": LanguageConfig("bn", "Bengali", "বাংলা", False),
}

DEFAULT_LANGUAGE = "en"

# Hindi Unicode range for Hinglish detection
HINDI_UNICODE_START = "\u0900"
HINDI_UNICODE_END = "\u097F"
HINDI_CHAR_THRESHOLD = 3

# Common Hinglish markers
HINGLISH_MARKERS = [
    "hai", "hain", "nahi", "karo", "bolo", "aap", "mera",
    "tera", "yeh", "woh", "kya", "kyun", "matlab", "theek",
    "accha", "bilkul", "zaroor", "abhi", "baad", "pehle",
]