"""
translator.py
Translation layer for multilingual responses.
Translates agent responses while keeping source citations intact.
No external translation API required — uses dictionary-based
translation for common scam-related phrases in Hindi/Hinglish.
Future-ready for Google Translate / DeepL integration.
"""

from __future__ import annotations

from configs.config import get_logger

logger = get_logger(__name__)

# Common scam advisory phrases — English to Hindi
EN_TO_HI: dict[str, str] = {
    "Do not share OTP": "OTP शेयर न करें",
    "Disconnect the call": "कॉल काट दें",
    "Report to cybercrime": "साइबर क्राइम पर रिपोर्ट करें",
    "Do not transfer money": "पैसे ट्रांसफर न करें",
    "This is a scam": "यह एक धोखा है",
    "HIGH RISK DETECTED": "उच्च जोखिम पाया गया",
    "CRITICAL RISK DETECTED": "अत्यधिक जोखिम पाया गया",
    "Call 1930 immediately": "तुरंत 1930 पर कॉल करें",
    "No scam patterns detected": "कोई धोखाधड़ी नहीं पाई गई",
    "Exercise caution": "सावधानी बरतें",
}

# Hinglish versions
EN_TO_HINGLISH: dict[str, str] = {
    "Do not share OTP": "OTP share mat karo",
    "Disconnect the call": "Call kat do",
    "Report to cybercrime": "Cybercrime portal pe report karo",
    "Do not transfer money": "Paise transfer mat karo",
    "This is a scam": "Yeh ek fraud hai",
    "HIGH RISK DETECTED": "High risk mila hai",
    "CRITICAL RISK DETECTED": "Bahut zyada risk hai",
    "Call 1930 immediately": "Abhi 1930 pe call karo",
    "No scam patterns detected": "Koi fraud nahi mila",
    "Exercise caution": "Savdhaan rahein",
}


def translate_response(text: str, target_language: str) -> str:
    """
    Translate response text to target language.
    Keeps source citations and document names untranslated.

    Args:
        text: Response text in English
        target_language: Target language code ('hi', 'hinglish', 'en')

    Returns:
        Translated text
    """
    if not text or target_language == "en":
        return text

    translation_map = (
        EN_TO_HI if target_language == "hi" else EN_TO_HINGLISH
    )

    translated = text
    for english_phrase, translated_phrase in translation_map.items():
        translated = translated.replace(english_phrase, translated_phrase)

    logger.debug(
        "Translated response to %s (%d chars)", target_language, len(translated)
    )
    return translated


def get_language_greeting(language: str) -> str:
    """Return greeting in the detected language."""
    greetings = {
        "en": "Hello! I am your Digital Arrest Scam Shield assistant.",
        "hi": "नमस्ते! मैं आपका डिजिटल अरेस्ट स्कैम शील्ड सहायक हूं।",
        "hinglish": "Hello! Main aapka Digital Arrest Scam Shield assistant hoon.",
    }
    return greetings.get(language, greetings["en"])