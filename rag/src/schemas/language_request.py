"""
language_request.py
Pydantic schemas for language detection request contracts.
Ready for FastAPI integration on Day 4.
"""

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


class LanguageDetectRequest(BaseModel):
    """Schema for language detection requests."""

    text: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Text to detect language for"
    )


class LanguageUpdateRequest(BaseModel):
    """Schema for updating session language preference."""

    session_id: str = Field(..., description="Session ID to update")
    language: str = Field(
        ...,
        description="New language preference. Options: en, hi, hinglish"
    )