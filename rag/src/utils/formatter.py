"""
formatter.py
Formats agent responses into structured, readable output.
Produces both JSON and Markdown formats.
"""

from __future__ import annotations

from src.agents.response_models import AgentResponse, RiskLevel
from configs.config import get_logger

logger = get_logger(__name__)

DISCLAIMER = (
    "This assessment is AI-generated based on known scam patterns and "
    "government advisories. Always verify with official sources. "
    "In emergency, call 1930 or 100."
)

RISK_EMOJI = {
    RiskLevel.LOW: "🟢",
    RiskLevel.MEDIUM: "🟡",
    RiskLevel.HIGH: "🔴",
    RiskLevel.CRITICAL: "🚨",
}


def format_response_markdown(response: AgentResponse) -> str:
    """
    Format AgentResponse into a readable Markdown string.

    Args:
        response: Structured AgentResponse from the agent

    Returns:
        Formatted Markdown string
    """
    emoji = RISK_EMOJI.get(response.risk_level, "⚪")
    lines: list[str] = []

    lines.append(f"## {emoji} Risk Assessment: {response.risk_level.value}")
    lines.append("")

    if response.scam_type:
        lines.append(f"**Scam Type:** {response.scam_type}")

    lines.append(f"**Risk Score:** {response.risk_score:.0%}")
    lines.append(f"**Confidence:** {response.confidence:.0%}")
    lines.append(f"**Language:** {response.language.value.title()}")
    lines.append("")

    lines.append("### Explanation")
    lines.append(response.explanation)
    lines.append("")

    if response.safety_checklist:
        lines.append("### Recommended Actions")
        for item in response.safety_checklist:
            lines.append(f"- {item}")
        lines.append("")

    if response.supporting_documents:
        lines.append("### Sources")
        for doc in response.supporting_documents:
            lines.append(f"- {doc}")
        lines.append("")

    if response.emergency_contacts:
        lines.append("### Emergency Contacts")
        for name, contact in response.emergency_contacts.items():
            lines.append(f"- **{name.replace('_', ' ').title()}:** {contact}")
        lines.append("")

    lines.append("---")
    lines.append(f"*{DISCLAIMER}*")

    return "\n".join(lines)


def format_response_dict(response: AgentResponse) -> dict:
    """
    Format AgentResponse into a dict ready for JSON serialization.
    Used by the service layer for API responses later.
    """
    return {
        "risk_level": response.risk_level.value,
        "risk_score": round(response.risk_score, 3),
        "confidence": round(response.confidence, 3),
        "scam_type": response.scam_type,
        "is_scam": response.is_scam,
        "language": response.language.value,
        "explanation": response.explanation,
        "safety_checklist": response.safety_checklist,
        "supporting_documents": response.supporting_documents,
        "emergency_contacts": response.emergency_contacts,
        "disclaimer": DISCLAIMER,
    }