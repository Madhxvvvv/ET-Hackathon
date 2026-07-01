"""
digital_arrest_agent.py
Main LangChain agent for the Digital Arrest Scam Shield.
Orchestrates the four tools and returns a structured AgentResponse.
"""

from __future__ import annotations

import time
from typing import Optional

from configs.config import get_logger
from src.agents.response_models import (
    AgentResponse,
    ConversationRiskResult,
    Language,
    RiskLevel,
    ScamPatternResult,
)
from src.agents.scam_patterns import EMERGENCY_CONTACTS
from src.agents.tools import (
    conversation_risk_analyzer,
    government_advisory_retriever,
    safety_recommendation_tool,
    scam_pattern_detector,
)

logger = get_logger(__name__)


def _map_risk_score_to_level(score: float) -> RiskLevel:
    if score >= 0.85:
        return RiskLevel.CRITICAL
    if score >= 0.65:
        return RiskLevel.HIGH
    if score >= 0.35:
        return RiskLevel.MEDIUM
    return RiskLevel.LOW


def analyze(
    user_message: str,
    is_transcript: bool = False,
) -> AgentResponse:
    """
    Main entry point for the agent.

    Args:
        user_message: The user's query, suspicious message, or call transcript.
        is_transcript: Set True if user_message is a full call transcript.

    Returns:
        AgentResponse with risk level, explanation, checklist, and contacts.
    """
    start = time.time()
    logger.info(
        "Agent.analyze called | transcript=%s | length=%d",
        is_transcript,
        len(user_message),
    )

    if not user_message or not user_message.strip():
        return AgentResponse(
            explanation="No input provided.",
            risk_level=RiskLevel.LOW,
        )

    # Step 1 — pattern detection
    if is_transcript:
        risk_raw = conversation_risk_analyzer.invoke(user_message)
        risk_result = ConversationRiskResult(**risk_raw)

        pattern_result = ScamPatternResult(
            detected_patterns=risk_result.detected_patterns,
            risk_score=0.0,
            confidence=risk_result.confidence,
            language=Language.UNKNOWN,
        )
        risk_level = risk_result.risk_level
        recommended_actions = risk_result.recommended_actions
        advisory_sources = risk_result.supporting_documents

    else:
        pattern_raw = scam_pattern_detector.invoke(user_message)
        pattern_result = ScamPatternResult(**pattern_raw)
        risk_level = _map_risk_score_to_level(pattern_result.risk_score)
        recommended_actions = []
        advisory_sources = []

    # Step 2 — retrieve advisories if risk is not LOW
    advisory_docs: list[str] = []
    if risk_level != RiskLevel.LOW or pattern_result.detected_patterns:
        query = (
            " ".join(pattern_result.detected_patterns)
            if pattern_result.detected_patterns
            else user_message[:200]
        )
        advisory_raw = government_advisory_retriever.invoke(query)
        advisory_docs = advisory_raw.get("documents", [])
        advisory_sources = advisory_raw.get("sources", [])

    # Step 3 — safety recommendations
    safety_raw = safety_recommendation_tool.invoke(risk_level.value)
    checklist = safety_raw.get("action_checklist", [])
    if not recommended_actions:
        recommended_actions = checklist

    # Step 4 — build explanation
    scam_type = (
        pattern_result.detected_patterns[0].replace("_", " ").title()
        if pattern_result.detected_patterns
        else None
    )

    if risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL):
        explanation = (
            f"⚠️ {risk_level.value} RISK DETECTED. "
            f"This appears to be a {scam_type or 'digital scam'}. "
            f"Detected indicators: {', '.join(pattern_result.detected_patterns)}. "
            f"Do NOT transfer money or share personal details."
        )
    elif risk_level == RiskLevel.MEDIUM:
        explanation = (
            f"This message shows some suspicious characteristics "
            f"({', '.join(pattern_result.detected_patterns)}). "
            f"Exercise caution and verify independently."
        )
    else:
        if pattern_result.detected_patterns:
            explanation = (
                f"Low risk detected but found these indicators: "
                f"{', '.join(pattern_result.detected_patterns)}. Stay alert."
            )
        else:
            explanation = "No scam patterns detected. This appears to be a safe message."

    response = AgentResponse(
        scam_type=scam_type,
        risk_level=risk_level,
        risk_score=pattern_result.risk_score,
        confidence=pattern_result.confidence,
        explanation=explanation,
        supporting_documents=advisory_sources,
        safety_checklist=checklist,
        emergency_contacts=(
            EMERGENCY_CONTACTS
            if risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL)
            else {}
        ),
        language=pattern_result.language,
        is_scam=risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL),
    )

    logger.info(
        "Agent completed | risk=%s | scam=%s | time=%.2fs",
        risk_level.value,
        response.is_scam,
        time.time() - start,
    )
    return response