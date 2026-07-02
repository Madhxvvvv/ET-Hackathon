"""
chat_response.py
Pydantic schemas for chat API response contracts.
Ready for FastAPI integration on Day 4.
"""

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


class ChatResponse(BaseModel):
    """Schema for chat API responses."""

    session_id: str
    language: str
    risk_level: str
    is_scam: bool
    response: str
    latency_seconds: float
    conversation_length: Optional[int] = None


class HistoryResponse(BaseModel):
    """Schema for conversation history responses."""

    session_id: str
    language: str
    messages: list[dict]
    message_count: int


class GreetingResponse(BaseModel):
    """Schema for greeting responses."""

    session_id: str
    language: str
    response: str