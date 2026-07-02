"""
test_day3.py
pytest tests for Day 3 — multilingual, complaint generation,
session management, response pipeline, schemas, services.
"""

from __future__ import annotations

import pytest

from src.utils.language_config import SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE
from src.utils.language_detector import detect_language
from src.utils.translator import translate_response, get_language_greeting
from src.utils.formatter import format_response_markdown, format_response_dict
from src.complaint_generator import ComplaintData, generate_complaint_json, generate_complaint_markdown
from src.session_manager import SessionManager, session_manager
from src.response_pipeline import run_pipeline
from src.services.chat_service import ChatService
from src.services.complaint_service import ComplaintService
from src.services.retrieval_service import RetrievalService
from src.services.session_service import SessionService
from src.schemas.chat_request import ChatRequest, TranscriptRequest
from src.schemas.chat_response import ChatResponse
from src.schemas.complaint_request import ComplaintRequest
from src.schemas.complaint_response import ComplaintResponse
from src.schemas.language_request import LanguageDetectRequest, LanguageUpdateRequest
from src.schemas.language_response import LanguageDetectResponse
from src.agents.response_models import AgentResponse, RiskLevel, Language


# ---------------------------------------------------------------------------
# Language Detection
# ---------------------------------------------------------------------------

def test_detect_english():
    assert detect_language("Hello, I received a suspicious call") == "en"


def test_detect_hindi():
    assert detect_language("मुझे एक संदिग्ध कॉल आई") == "hi"


def test_detect_hinglish_roman():
    assert detect_language("Mujhe ek suspicious call aaya hai yeh fraud hai") == "hinglish"


def test_detect_hinglish_mixed_script():
    result = detect_language("Hello मैं CBI se bol raha hoon")
    assert result in ("hi", "hinglish", "en")


def test_detect_empty_input():
    assert detect_language("") == DEFAULT_LANGUAGE


def test_detect_language_switching():
    assert detect_language("What is UPI fraud?") == "en"
    assert detect_language("UPI fraud kya hai yeh batao") == "hinglish"


# ---------------------------------------------------------------------------
# Translation
# ---------------------------------------------------------------------------

def test_translate_to_hindi():
    result = translate_response("Do not share OTP", "hi")
    assert result != "Do not share OTP"
    assert len(result) > 0


def test_translate_to_hinglish():
    result = translate_response("Do not share OTP", "hinglish")
    assert "OTP" in result


def test_translate_english_unchanged():
    text = "Do not share OTP"
    assert translate_response(text, "en") == text


def test_translate_empty_string():
    assert translate_response("", "hi") == ""


def test_greeting_english():
    greeting = get_language_greeting("en")
    assert "assistant" in greeting.lower()


def test_greeting_hindi():
    greeting = get_language_greeting("hi")
    assert len(greeting) > 0


def test_greeting_hinglish():
    greeting = get_language_greeting("hinglish")
    assert len(greeting) > 0


# ---------------------------------------------------------------------------
# Formatter
# ---------------------------------------------------------------------------

def test_format_markdown_high_risk():
    response = AgentResponse(
        risk_level=RiskLevel.HIGH,
        risk_score=0.85,
        confidence=0.9,
        is_scam=True,
        explanation="This is a scam",
        scam_type="Digital Arrest",
        safety_checklist=["Do not transfer money"],
        emergency_contacts={"helpline": "1930"},
        language=Language.ENGLISH,
    )
    md = format_response_markdown(response)
    assert "HIGH" in md
    assert "1930" in md
    assert "disclaimer" in md.lower() or "assessment" in md.lower()


def test_format_dict_structure():
    response = AgentResponse(
        risk_level=RiskLevel.LOW,
        risk_score=0.1,
        confidence=0.8,
        is_scam=False,
        language=Language.ENGLISH,
    )
    d = format_response_dict(response)
    assert "risk_level" in d
    assert "disclaimer" in d
    assert d["is_scam"] is False


# ---------------------------------------------------------------------------
# Complaint Generator
# ---------------------------------------------------------------------------

def test_complaint_json_structure():
    data = ComplaintData(
        scam_type="Digital Arrest Scam",
        victim_name="Test User",
        incident_description="Caller claimed to be CBI officer",
        money_lost=50000.0,
        suspect_phone="9999999999",
    )
    result = generate_complaint_json(data)
    assert "victim_information" in result
    assert "incident_details" in result
    assert "financial_loss" in result
    assert "recommended_next_steps" in result


def test_complaint_markdown_contains_sections():
    data = ComplaintData(
        scam_type="OTP Fraud",
        incident_description="Someone asked for OTP",
    )
    md = generate_complaint_markdown(data)
    assert "Victim Information" in md
    assert "Incident Details" in md
    assert "cybercrime.gov.in" in md


def test_complaint_zero_money_lost():
    data = ComplaintData(
        scam_type="KYC Scam",
        incident_description="KYC update scam attempt",
        money_lost=0.0,
    )
    result = generate_complaint_json(data)
    assert result["financial_loss"]["amount"] == 0.0


# ---------------------------------------------------------------------------
# Session Manager
# ---------------------------------------------------------------------------

def test_session_create():
    sm = SessionManager()
    session = sm.create_session(language="en")
    assert session.session_id is not None
    assert session.language == "en"


def test_session_get():
    sm = SessionManager()
    session = sm.create_session()
    retrieved = sm.get_session(session.session_id)
    assert retrieved is not None
    assert retrieved.session_id == session.session_id


def test_session_add_message():
    sm = SessionManager()
    session = sm.create_session()
    session.add_message("user", "Hello", language="en")
    assert len(session.messages) == 1
    assert session.messages[0].role == "user"


def test_session_get_history():
    sm = SessionManager()
    session = sm.create_session()
    session.add_message("user", "test message")
    history = session.get_history()
    assert len(history) == 1
    assert "role" in history[0]
    assert "content" in history[0]


def test_session_not_found():
    sm = SessionManager()
    result = sm.get_session("nonexistent-id")
    assert result is None


def test_session_delete():
    sm = SessionManager()
    session = sm.create_session()
    sm.delete_session(session.session_id)
    assert sm.get_session(session.session_id) is None


def test_session_get_or_create_new():
    sm = SessionManager()
    session = sm.get_or_create(None)
    assert session.session_id is not None


def test_session_cleanup():
    sm = SessionManager()
    sm.create_session()
    count = sm.cleanup_expired()
    assert isinstance(count, int)


# ---------------------------------------------------------------------------
# Response Pipeline
# ---------------------------------------------------------------------------

def test_pipeline_english_scam():
    result = run_pipeline(
        "CBI officer here, you are under digital arrest, transfer money now"
    )
    assert "risk_level" in result
    assert "response" in result
    assert "language" in result


def test_pipeline_hindi_input():
    result = run_pipeline("मुझे CBI से call आई है digital arrest का notice")
    assert result["language"] in ("hi", "hinglish", "en")


def test_pipeline_safe_message():
    result = run_pipeline("What is my account balance?")
    assert result["risk_level"] == "LOW"
    assert result["is_scam"] is False


def test_pipeline_returns_latency():
    result = run_pipeline("Hello")
    assert "latency_seconds" in result
    assert result["latency_seconds"] > 0


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------

def test_chat_service_basic():
    service = ChatService()
    result = service.chat("Someone called saying I am under digital arrest")
    assert "session_id" in result
    assert "risk_level" in result


def test_chat_service_greeting():
    service = ChatService()
    result = service.get_greeting(language="en")
    assert "session_id" in result
    assert len(result["response"]) > 0


def test_chat_service_history():
    service = ChatService()
    result = service.chat("test message")
    history = service.get_history(result["session_id"])
    assert "messages" in history
    assert history["message_count"] > 0


def test_complaint_service_markdown():
    service = ComplaintService()
    result = service.generate(
        scam_type="Digital Arrest Scam",
        incident_description="CBI officer called and demanded money",
        money_lost=10000.0,
    )
    assert "complaint" in result
    assert result["helpline"] == "1930"


def test_complaint_service_json():
    service = ComplaintService()
    result = service.generate(
        scam_type="OTP Fraud",
        incident_description="Someone asked for OTP",
        output_format="json",
    )
    assert isinstance(result["complaint"], dict)


def test_retrieval_service_basic():
    service = RetrievalService()
    result = service.search("digital arrest scam")
    assert "results" in result
    assert "count" in result


def test_retrieval_service_empty_query():
    service = RetrievalService()
    result = service.search("")
    assert result["count"] == 0


def test_session_service_create():
    service = SessionService()
    result = service.create(language="en")
    assert "session_id" in result


def test_session_service_get():
    service = SessionService()
    created = service.create()
    retrieved = service.get(created["session_id"])
    assert retrieved["session_id"] == created["session_id"]


def test_session_service_delete():
    service = SessionService()
    created = service.create()
    result = service.delete(created["session_id"])
    assert result["deleted"] is True


def test_session_service_update_language():
    service = SessionService()
    created = service.create(language="en")
    result = service.update_language(created["session_id"], "hi")
    assert result["language"] == "hi"


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

def test_chat_request_valid():
    req = ChatRequest(message="Hello", session_id=None)
    assert req.message == "Hello"
    assert req.is_transcript is False


def test_chat_request_invalid_empty():
    with pytest.raises(Exception):
        ChatRequest(message="")


def test_complaint_request_valid():
    req = ComplaintRequest(
        scam_type="OTP Fraud",
        incident_description="Someone asked for my OTP over phone",
    )
    assert req.scam_type == "OTP Fraud"


def test_language_detect_request():
    req = LanguageDetectRequest(text="Hello world")
    assert req.text == "Hello world"


def test_language_config_has_english_and_hindi():
    assert "en" in SUPPORTED_LANGUAGES
    assert "hi" in SUPPORTED_LANGUAGES
    assert SUPPORTED_LANGUAGES["en"].supported is True
    assert SUPPORTED_LANGUAGES["hi"].supported is True