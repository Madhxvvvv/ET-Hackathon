"""
complaint_generator.py
Generates structured cybercrime complaint drafts.
Produces both JSON and Markdown formats.
Does NOT submit to any portal.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from configs.config import get_logger

logger = get_logger(__name__)


@dataclass
class ComplaintData:
    scam_type: str
    victim_name: str = "Not Provided"
    victim_phone: str = "Not Provided"
    victim_email: str = "Not Provided"
    incident_date: str = ""
    incident_description: str = ""
    money_lost: float = 0.0
    currency: str = "INR"
    suspect_phone: str = "Not Provided"
    suspect_account: str = "Not Provided"
    bank_name: str = "Not Provided"
    transaction_id: str = "Not Provided"
    evidence_available: list[str] = field(default_factory=list)


def generate_complaint_json(data: ComplaintData) -> dict:
    """Generate structured complaint as JSON dict."""
    return {
        "complaint_metadata": {
            "generated_at": datetime.utcnow().isoformat(),
            "complaint_type": "Cybercrime",
            "portal": "cybercrime.gov.in",
            "helpline": "1930",
        },
        "victim_information": {
            "name": data.victim_name,
            "phone": data.victim_phone,
            "email": data.victim_email,
        },
        "incident_details": {
            "scam_type": data.scam_type,
            "date": data.incident_date or datetime.utcnow().strftime("%Y-%m-%d"),
            "description": data.incident_description,
        },
        "financial_loss": {
            "amount": data.money_lost,
            "currency": data.currency,
            "suspect_account": data.suspect_account,
            "bank_name": data.bank_name,
            "transaction_id": data.transaction_id,
        },
        "suspect_information": {
            "phone": data.suspect_phone,
        },
        "evidence": {
            "available": data.evidence_available,
            "screenshots": "Attach screenshots separately",
            "call_logs": "Attach call logs separately",
        },
        "recommended_next_steps": [
            "File complaint at cybercrime.gov.in",
            "Call 1930 (Cyber Crime Helpline)",
            "Visit nearest police station with this complaint",
            "Preserve all evidence — screenshots, call logs, messages",
            "Contact your bank immediately if money was transferred",
        ],
    }


def generate_complaint_markdown(data: ComplaintData) -> str:
    """Generate user-readable complaint draft in Markdown."""
    complaint = generate_complaint_json(data)
    lines: list[str] = []

    lines.append("# Cybercrime Complaint Draft")
    lines.append(f"*Generated: {complaint['complaint_metadata']['generated_at']}*")
    lines.append("")
    lines.append("## Victim Information")
    lines.append(f"- **Name:** {data.victim_name}")
    lines.append(f"- **Phone:** {data.victim_phone}")
    lines.append(f"- **Email:** {data.victim_email}")
    lines.append("")
    lines.append("## Incident Details")
    lines.append(f"- **Scam Type:** {data.scam_type}")
    lines.append(f"- **Date:** {complaint['incident_details']['date']}")
    lines.append(f"- **Description:** {data.incident_description}")
    lines.append("")
    lines.append("## Financial Loss")
    lines.append(f"- **Amount Lost:** {data.currency} {data.money_lost}")
    lines.append(f"- **Suspect Account:** {data.suspect_account}")
    lines.append(f"- **Bank:** {data.bank_name}")
    lines.append(f"- **Transaction ID:** {data.transaction_id}")
    lines.append("")
    lines.append("## Suspect Information")
    lines.append(f"- **Phone:** {data.suspect_phone}")
    lines.append("")
    lines.append("## Evidence Available")
    for ev in data.evidence_available:
        lines.append(f"- {ev}")
    if not data.evidence_available:
        lines.append("- None specified")
    lines.append("")
    lines.append("## Next Steps")
    for step in complaint["recommended_next_steps"]:
        lines.append(f"1. {step}")
    lines.append("")
    lines.append("---")
    lines.append("*Submit this complaint at cybercrime.gov.in or call 1930*")

    return "\n".join(lines)