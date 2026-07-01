"""Pydantic schemas for the currency detection endpoints."""

from pydantic import BaseModel, Field


class DetectResponse(BaseModel):
    label: str = Field(..., examples=["genuine", "counterfeit"])
    confidence: float = Field(..., ge=0.0, le=1.0, examples=[0.97])
    model_version: str = Field(default="efficientnet-b0-v1")
