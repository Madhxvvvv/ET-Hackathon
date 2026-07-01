"""
test_day2_agent.py
pytest tests for Day 2 — agent, tools, prompts, response models.
Covers English, Hindi, mixed language, false positives, edge cases.
"""

from __future__ import annotations

import pytest

from src.agents.response_models import AgentResponse, Language, RiskLevel
from src.agents.scam_patterns import EMERGENCY_CONTACTS, SCAM_PATTERNS
from src.agents.tools import (
    conversation_risk_analyzer,
    government_advisory_retriever,
    safety_recommendation_tool,
    scam_pattern_detector,
)
from src.agents.digital_arrest_agent import analyze


# ---------------------------------------------------------------------------
# Synthetic test data
# ---------------------------------------------------------------------------

ENGLISH_SCAM = (
    "This is CBI officer Singh. You are under digital arrest. "
    "Your account has been frozen due to money laundering. "
    "Transfer Rs 50000 immediately to clear your name."
)

HINDI_SCAM = (
    "Main CBI se bol raha hoon. Aapka account freeze ho gaya hai. "
    "Digital arrest ka notice aaya hai. Abhi paise transfer karo "
    "warna aapko jail jana padega."
)

MIXED_SCAM = (
    "Hello sir, main RBI officer hoon. Your KYC has expired. "
    "Aapko abhi OTP share karna hoga warna account block ho jayega."
)

SAFE_CONVERSATION = (
    "Hi, I wanted to check my account balance and get a mini statement. "
    "Can you help me with that?"
)

NORMAL_BANKING = (
    "I would like to open a new savings account. "
    "What documents do I need?"
)

UPI_SCAM = (
    "Sir please scan this QR code to receive your refund of Rs 5000. "
    "Enter your UPI PIN to complete the transaction."
)

OTP_SCAM = (
    "Your bank account will be blocked. Share OTP received on your "
    "phone to verify your identity and unblock the account."
)

DIGITAL_ARREST_TRANSCRIPT = """
Caller: This is officer Sharma from CBI headquarters.
Victim: Yes?
Caller: You are under digital arrest for money laundering charges.
Victim: What? I haven't done anything.
Caller: Your account has been frozen. Transfer Rs 2 lakh immediately.
Victim: I don't have that money.
Caller: Then you will be arrested. Stay on call — digital arrest.
"""

EMPTY_INPUT = ""
LARGE_TRANSCRIPT = DIGITAL_ARREST_TRANSCRIPT * 50


# ---------------------------------------------------------------------------
# Tool 1: ScamPatternDetector
# ---------------------------------------------------------------------------

def test_scam_detector_english_scam():
    result = scam_pattern_detector.invoke(ENGLISH_SCAM)
    assert result["risk_score"] > 0.5
    assert len(result["detected_patterns"]) > 0
    assert result["confidence"] > 0.5


def test_scam_detector_hindi_scam():
    result = scam_pattern_detector.invoke(HINDI_SCAM)
    assert result["risk_score"] > 0.3
    assert len(result["detected_patterns"]) > 0


def test_scam_detector_mixed_language():
    result = scam_pattern_detector.invoke(MIXED_SCAM)
    assert result["risk_score"] > 0.3
    assert len(result["detected_patterns"]) > 0


def test_scam_detector_safe_conversation():
    result = scam_pattern_detector.invoke(SAFE_CONVERSATION)
    assert result["risk_score"] == 0.0
    assert result["detected_patterns"] == []


def test_scam_detector_empty_input():
    result = scam_pattern_detector.invoke(EMPTY_INPUT)
    assert result["risk_score"] == 0.0


def test_scam_detector_upi_scam():
    result = scam_pattern_detector.invoke(UPI_SCAM)
    assert "upi_fraud" in result["detected_patterns"]


def test_scam_detector_otp_scam():
    result = scam_pattern_detector.invoke(OTP_SCAM)
    assert "otp_fraud" in result["detected_patterns"]


# ---------------------------------------------------------------------------
# Tool 2: GovernmentAdvisoryRetriever
# ---------------------------------------------------------------------------

def test_advisory_retriever_returns_results():
    result = government_advisory_retriever.invoke("digital arrest scam")
    assert isinstance(result["documents"], list)
    assert isinstance(result["sources"], list)


def test_advisory_retriever_empty_query():
    result = government_advisory_retriever.invoke("")
    assert result["confidence"] == 0.0


def test_advisory_retriever_otp_query():
    result = government_advisory_retriever.invoke("OTP fraud awareness")
    assert len(result["documents"]) > 0


# ---------------------------------------------------------------------------
# Tool 3: SafetyRecommendationTool
# ---------------------------------------------------------------------------

def test_safety_tool_high_risk():
    result = safety_recommendation_tool.invoke("HIGH")
    assert len(result["action_checklist"]) > 0
    assert result["urgency_level"] == "HIGH"
    assert "1930" in str(result["emergency_contacts"])


def test_safety_tool_critical_risk():
    result = safety_recommendation_tool.invoke("CRITICAL")
    assert result["urgency_level"] == "CRITICAL"
    assert len(result["action_checklist"]) >= 5


def test_safety_tool_low_risk():
    result = safety_recommendation_tool.invoke("LOW")
    assert result["urgency_level"] == "LOW"


def test_safety_tool_invalid_input():
    # should not crash — falls back to MEDIUM
    result = safety_recommendation_tool.invoke("UNKNOWN_LEVEL")
    assert result["urgency_level"] == "MEDIUM"


# ---------------------------------------------------------------------------
# Tool 4: ConversationRiskAnalyzer
# ---------------------------------------------------------------------------

def test_conversation_analyzer_high_risk_transcript():
    result = conversation_risk_analyzer.invoke(DIGITAL_ARREST_TRANSCRIPT)
    assert result["risk_level"] in ("HIGH", "CRITICAL")
    assert result["confidence"] > 0.5
    assert len(result["detected_patterns"]) > 0


def test_conversation_analyzer_safe_conversation():
    result = conversation_risk_analyzer.invoke(SAFE_CONVERSATION)
    assert result["risk_level"] in ("LOW", "MEDIUM")


def test_conversation_analyzer_empty_input():
    result = conversation_risk_analyzer.invoke(EMPTY_INPUT)
    assert result["risk_level"] == "LOW"
    assert result["confidence"] == 0.0


def test_conversation_analyzer_large_transcript():
    # should not crash on large input
    result = conversation_risk_analyzer.invoke(LARGE_TRANSCRIPT)
    assert result["risk_level"] in ("HIGH", "CRITICAL")


# ---------------------------------------------------------------------------
# Main Agent
# ---------------------------------------------------------------------------

def test_agent_english_scam():
    response = analyze(ENGLISH_SCAM)
    assert isinstance(response, AgentResponse)
    assert response.is_scam is True
    assert response.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL)


def test_agent_hindi_scam():
    response = analyze(HINDI_SCAM)
    assert response.risk_level in (RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL)


def test_agent_safe_message():
    response = analyze(SAFE_CONVERSATION)
    assert response.is_scam is False
    assert response.risk_level == RiskLevel.LOW


def test_agent_transcript_mode():
    response = analyze(DIGITAL_ARREST_TRANSCRIPT, is_transcript=True)
    assert response.is_scam is True
    assert len(response.safety_checklist) > 0


def test_agent_empty_input():
    response = analyze(EMPTY_INPUT)
    assert response.risk_level == RiskLevel.LOW
    assert response.is_scam is False


def test_agent_returns_emergency_contacts_for_high_risk():
    response = analyze(ENGLISH_SCAM)
    assert "cybercrime_helpline" in response.emergency_contacts


def test_agent_explanation_not_empty():
    response = analyze(ENGLISH_SCAM)
    assert len(response.explanation) > 0


# ---------------------------------------------------------------------------
# Response Models
# ---------------------------------------------------------------------------

def test_agent_response_model_validation():
    r = AgentResponse(
        risk_level=RiskLevel.HIGH,
        risk_score=0.8,
        confidence=0.9,
        is_scam=True,
    )
    assert r.risk_score == 0.8
    assert r.is_scam is True


def test_scam_patterns_not_empty():
    assert len(SCAM_PATTERNS) > 0
    for category, keywords in SCAM_PATTERNS.items():
        assert len(keywords) > 0


def test_emergency_contacts_present():
    assert "cybercrime_helpline" in EMERGENCY_CONTACTS
    assert EMERGENCY_CONTACTS["cybercrime_helpline"] == "1930"