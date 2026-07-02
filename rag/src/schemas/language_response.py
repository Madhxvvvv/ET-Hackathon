"""
language_response.py
Pydantic schemas for language detection response contracts.
Ready for FastAPI integration on Day 4.
"""

from __future__ import annotations

from pydantic import BaseModel


class LanguageDetectResponse(BaseModel):
    """Schema for language detection responses."""

    text_preview: str
    detected_language: str
    language_display_name: str
    is_supported: bool


class LanguageUpdateResponse(BaseModel):
    """Schema for language update responses."""

    session_id: str
    language: str
    updated: bool