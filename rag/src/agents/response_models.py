"""
response_models.py
Pydantic models for structured agent responses.
All tool outputs and final agent responses conform to these models.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Language(str, Enum):
    ENGLISH = "english"
    HINDI = "hindi"
    MIXED = "mixed"
    UNKNOWN = "unknown"


class ScamPatternResult(BaseModel):
    """Output of the ScamPatternDetector tool."""

    detected_patterns: list[str] = Field(
        default_factory=list,
        description="List of scam pattern categories detected"
    )
    risk_score: float = Field(
        ge=0.0, le=1.0,
        description="Risk score between 0.0 and 1.0"
    )
    confidence: float = Field(
        ge=0.0, le=1.0,
        description="Confidence in the detection"
    )
    supporting_evidence: list[str] = Field(
        default_factory=list,
        description="Exact phrases that triggered detection"
    )
    language: Language = Language.UNKNOWN


class AdvisoryResult(BaseModel):
    """Output of the GovernmentAdvisoryRetriever tool."""

    documents: list[str] = Field(
        default_factory=list,
        description="Relevant advisory document chunks"
    )
    sources: list[str] = Field(
        default_factory=list,
        description="Source document names"
    )
    summary: str = ""
    confidence: float = Field(ge=0.0, le=1.0, default=0.0)


class SafetyRecommendation(BaseModel):
    """Output of the SafetyRecommendationTool."""

    action_checklist: list[str] = Field(default_factory=list)
    urgency_level: RiskLevel = RiskLevel.LOW
    reference_documents: list[str] = Field(default_factory=list)
    emergency_contacts: dict[str, str] = Field(default_factory=dict)


class ConversationRiskResult(BaseModel):
    """Output of the ConversationRiskAnalyzer tool."""

    risk_level: RiskLevel = RiskLevel.LOW
    confidence: float = Field(ge=0.0, le=1.0, default=0.0)
    detected_patterns: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)
    supporting_documents: list[str] = Field(default_factory=list)


class AgentResponse(BaseModel):
    """Final structured response returned by the agent."""

    scam_type: Optional[str] = None
    risk_level: RiskLevel = RiskLevel.LOW
    risk_score: float = Field(ge=0.0, le=1.0, default=0.0)
    confidence: float = Field(ge=0.0, le=1.0, default=0.0)
    explanation: str = ""
    supporting_documents: list[str] = Field(default_factory=list)
    safety_checklist: list[str] = Field(default_factory=list)
    emergency_contacts: dict[str, str] = Field(default_factory=dict)
    language: Language = Language.UNKNOWN
    is_scam: bool = False