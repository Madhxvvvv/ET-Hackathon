"""
chat_request.py
Pydantic schemas for chat API request contracts.
Ready for FastAPI integration on Day 4.
"""

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Schema for incoming chat requests."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="User message or call transcript"
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Existing session ID. Creates new session if not provided."
    )
    is_transcript: bool = Field(
        default=False,
        description="Set True if message is a full call transcript"
    )
    language: Optional[str] = Field(
        default=None,
        description="Override language detection. Options: en, hi, hinglish"
    )
    output_format: str = Field(
        default="markdown",
        description="Response format. Options: markdown, dict"
    )


class TranscriptRequest(BaseModel):
    """Schema for full call transcript analysis."""

    transcript: str = Field(
        ...,
        min_length=1,
        max_length=20000,
        description="Full conversation transcript"
    )
    session_id: Optional[str] = None
    language: Optional[str] = None