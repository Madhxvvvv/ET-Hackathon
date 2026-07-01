"""
tools.py
Four production-ready LangChain tools for the Digital Arrest Scam Shield.

Tool 1: ScamPatternDetector
Tool 2: GovernmentAdvisoryRetriever
Tool 3: SafetyRecommendationTool
Tool 4: ConversationRiskAnalyzer
"""

from __future__ import annotations

import time
from typing import Optional

from langchain.tools import tool

from configs.config import DEFAULT_TOP_K, get_logger
from src.agents.response_models import (
    AdvisoryResult,
    AgentResponse,
    ConversationRiskResult,
    Language,
    RiskLevel,
    SafetyRecommendation,
    ScamPatternResult,
)
from src.agents.scam_patterns import (
    EMERGENCY_CONTACTS,
    SAFE_KEYWORDS,
    SCAM_PATTERNS,
)

logger = get_logger(__name__)


def _detect_language(text: str) -> Language:
    """Detect if text is English, Hindi, or mixed."""
    try:
        from langdetect import detect
        lang = detect(text)
        if lang == "hi":
            return Language.HINDI
        if lang == "en":
            return Language.ENGLISH
        return Language.MIXED
    except Exception:
        # fallback: check for Hindi Unicode range
        hindi_chars = sum(1 for c in text if "\u0900" <= c <= "\u097F")
        if hindi_chars > 3:
            return Language.HINDI
        return Language.ENGLISH


def _normalize_text(text: str) -> str:
    """Lowercase and strip for pattern matching."""
    return text.lower().strip()


@tool
def scam_pattern_detector(user_message: str) -> dict:
    """
    Analyzes a user message or caller transcript for digital scam patterns.
    Detects police/CBI/RBI impersonation, digital arrest, KYC scams,
    UPI fraud, OTP fraud, account freeze threats, and more.
    Returns risk score, detected patterns, confidence, and supporting evidence.
    """
    start = time.time()
    logger.info("ScamPatternDetector called with message length: %d", len(user_message))

    if not user_message or not user_message.strip():
        return ScamPatternResult(
            risk_score=0.0,
            confidence=0.0,
            language=Language.UNKNOWN
        ).model_dump()

    normalized = _normalize_text(user_message)
    language = _detect_language(user_message)

    detected_patterns: list[str] = []
    supporting_evidence: list[str] = []

    for pattern_name, keywords in SCAM_PATTERNS.items():
        for keyword in keywords:
            if keyword.lower() in normalized:
                if pattern_name not in detected_patterns:
                    detected_patterns.append(pattern_name)
                supporting_evidence.append(keyword)

    # check if it's a clearly safe conversation
    is_safe = any(kw in normalized for kw in SAFE_KEYWORDS)
    if is_safe and not detected_patterns:
        result = ScamPatternResult(
            detected_patterns=[],
            risk_score=0.0,
            confidence=0.95,
            supporting_evidence=[],
            language=language,
        )
        logger.info("Safe conversation detected in %.2fs", time.time() - start)
        return result.model_dump()

    # risk score based on number of pattern categories detected
    pattern_count = len(detected_patterns)
    if pattern_count == 0:
        risk_score = 0.0
        confidence = 0.8
    elif pattern_count == 1:
        risk_score = 0.4
        confidence = 0.75
    elif pattern_count == 2:
        risk_score = 0.65
        confidence = 0.82
    elif pattern_count == 3:
        risk_score = 0.80
        confidence = 0.88
    else:
        risk_score = min(0.95, 0.80 + (pattern_count - 3) * 0.05)
        confidence = 0.92

    result = ScamPatternResult(
        detected_patterns=detected_patterns,
        risk_score=risk_score,
        confidence=confidence,
        supporting_evidence=list(set(supporting_evidence)),
        language=language,
    )
    logger.info(
        "ScamPatternDetector: %d patterns, risk=%.2f in %.2fs",
        pattern_count, risk_score, time.time() - start
    )
    return result.model_dump()


@tool
def government_advisory_retriever(query: str) -> dict:
    """
    Retrieves official government advisories from CERT-In, RBI,
    Cyber Crime Portal, and MHA using the ChromaDB vector store.
    Use this to ground answers in real advisory content.
    Returns relevant document chunks, sources, and a summary.
    """
    start = time.time()
    logger.info("GovernmentAdvisoryRetriever called for query: %r", query[:80])

    if not query or not query.strip():
        return AdvisoryResult(confidence=0.0).model_dump()

    try:
        from src.retriever.retriever import retrieve
        chunks = retrieve(query, k=DEFAULT_TOP_K)

        if not chunks:
            logger.warning("No documents retrieved for query: %r", query[:80])
            return AdvisoryResult(confidence=0.0).model_dump()

        documents = [c.content for c in chunks]
        sources = list({c.source for c in chunks})
        avg_score = sum(c.score or 0.0 for c in chunks) / len(chunks)
        # ChromaDB returns L2 distance — lower = more similar
        # convert to 0-1 confidence (approximate)
        confidence = max(0.0, min(1.0, 1.0 - (avg_score / 2.0)))

        summary = f"Found {len(chunks)} relevant advisory chunks from: {', '.join(sources)}"

        result = AdvisoryResult(
            documents=documents,
            sources=sources,
            summary=summary,
            confidence=round(confidence, 3),
        )
        logger.info(
            "AdvisoryRetriever: %d chunks in %.2fs", len(chunks), time.time() - start
        )
        return result.model_dump()

    except Exception as e:
        logger.error("AdvisoryRetriever failed: %s", e)
        return AdvisoryResult(confidence=0.0, summary=f"Retrieval failed: {e}").model_dump()


@tool
def safety_recommendation_tool(risk_level: str) -> dict:
    """
    Generates safety recommendations and action checklist based on risk level.
    Input should be one of: LOW, MEDIUM, HIGH, CRITICAL.
    Returns an action checklist, urgency level, and emergency contacts.
    All advice is grounded in standard government advisory guidelines.
    """
    start = time.time()
    logger.info("SafetyRecommendationTool called with risk_level: %s", risk_level)

    try:
        level = RiskLevel(risk_level.upper())
    except ValueError:
        level = RiskLevel.MEDIUM

    base_checklist = [
        "Do not share OTP, PIN, or passwords with anyone",
        "Real government officers never demand money over call or video",
        "Disconnect the call immediately if you feel pressured",
        "Report suspicious calls to cybercrime.gov.in or call 1930",
    ]

    if level == RiskLevel.LOW:
        checklist = base_checklist
        urgency = RiskLevel.LOW

    elif level == RiskLevel.MEDIUM:
        checklist = base_checklist + [
            "Do not install any app suggested by the caller",
            "Do not click on any links sent via SMS or WhatsApp",
            "Verify officer identity by calling the official agency number",
        ]
        urgency = RiskLevel.MEDIUM

    elif level == RiskLevel.HIGH:
        checklist = base_checklist + [
            "STOP — do not transfer any money under any circumstances",
            "Do not install any remote access apps (AnyDesk, TeamViewer)",
            "Call a trusted family member or friend immediately",
            "File a complaint at cybercrime.gov.in right now",
            "Verify caller identity independently via official websites",
        ]
        urgency = RiskLevel.HIGH

    else:  # CRITICAL
        checklist = [
            "STOP ALL COMMUNICATION IMMEDIATELY",
            "Do not transfer money — hang up now",
            "Call 1930 (Cyber Crime Helpline) immediately",
            "Call 100 (Police) if you feel physically threatened",
            "Do not share screen or install any apps",
            "Inform a family member immediately",
            "Preserve all call logs and screenshots as evidence",
            "File complaint at cybercrime.gov.in",
        ]
        urgency = RiskLevel.CRITICAL

    result = SafetyRecommendation(
        action_checklist=checklist,
        urgency_level=urgency,
        reference_documents=["cybercrime.gov.in", "cert-in.org.in", "rbi.org.in"],
        emergency_contacts=EMERGENCY_CONTACTS,
    )
    logger.info("SafetyRecommendationTool completed in %.2fs", time.time() - start)
    return result.model_dump()


@tool
def conversation_risk_analyzer(transcript: str) -> dict:
    """
    Analyzes a full conversation transcript between a caller and victim.
    Detects digital arrest scam patterns across the entire conversation.
    Input: full transcript as a single string.
    Returns JSON with risk_level, confidence, detected_patterns,
    recommended_actions, and supporting_documents.
    """
    start = time.time()
    logger.info("ConversationRiskAnalyzer called, transcript length: %d", len(transcript))

    if not transcript or not transcript.strip():
        return ConversationRiskResult(
            risk_level=RiskLevel.LOW,
            confidence=0.0
        ).model_dump()

    # reuse scam pattern detector on full transcript
    pattern_result_raw = scam_pattern_detector.invoke(transcript)
    pattern_result = ScamPatternResult(**pattern_result_raw)

    # map risk score to risk level
    score = pattern_result.risk_score
    if score >= 0.85:
        risk_level = RiskLevel.CRITICAL
    elif score >= 0.65:
        risk_level = RiskLevel.HIGH
    elif score >= 0.35:
        risk_level = RiskLevel.MEDIUM
    else:
        risk_level = RiskLevel.LOW

    # get safety recommendations
    safety_raw = safety_recommendation_tool.invoke(risk_level.value)
    safety = SafetyRecommendation(**safety_raw)

    # get advisory documents
    query = " ".join(pattern_result.detected_patterns) or transcript[:200]
    advisory_raw = government_advisory_retriever.invoke(query)
    advisory = AdvisoryResult(**advisory_raw)

    result = ConversationRiskResult(
        risk_level=risk_level,
        confidence=pattern_result.confidence,
        detected_patterns=pattern_result.detected_patterns,
        recommended_actions=safety.action_checklist[:5],
        supporting_documents=advisory.sources,
    )
    logger.info(
        "ConversationRiskAnalyzer: %s risk in %.2fs",
        risk_level.value, time.time() - start
    )
    return result.model_dump()