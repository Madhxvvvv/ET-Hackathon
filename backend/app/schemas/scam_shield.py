"""Pydantic schemas for the Scam Shield RAG endpoints."""

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500, examples=["Is digital arrest legal in India?"])


class QueryResponse(BaseModel):
    answer: str
    sources: list[str] = Field(default_factory=list)
    confidence: float | None = None
