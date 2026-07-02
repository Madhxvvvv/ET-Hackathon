"""
complaint_service.py
Service layer for complaint generation.
Clean interface for future FastAPI integration.
"""

from __future__ import annotations

from configs.config import get_logger
from src.complaint_generator import (
    ComplaintData,
    generate_complaint_json,
    generate_complaint_markdown,
)

logger = get_logger(__name__)


class ComplaintService:
    """Handles complaint generation for various scam types."""

    def generate(
        self,
        scam_type: str,
        incident_description: str,
        victim_name: str = "Not Provided",
        victim_phone: str = "Not Provided",
        victim_email: str = "Not Provided",
        money_lost: float = 0.0,
        suspect_phone: str = "Not Provided",
        suspect_account: str = "Not Provided",
        bank_name: str = "Not Provided",
        transaction_id: str = "Not Provided",
        evidence_available: list[str] | None = None,
        output_format: str = "markdown",
    ) -> dict:
        """
        Generate a cybercrime complaint draft.

        Args:
            scam_type: Type of scam
            incident_description: What happened
            output_format: 'markdown' or 'json'

        Returns:
            Dict with complaint draft and metadata
        """
        data = ComplaintData(
            scam_type=scam_type,
            victim_name=victim_name,
            victim_phone=victim_phone,
            victim_email=victim_email,
            incident_description=incident_description,
            money_lost=money_lost,
            suspect_phone=suspect_phone,
            suspect_account=suspect_account,
            bank_name=bank_name,
            transaction_id=transaction_id,
            evidence_available=evidence_available or [],
        )

        if output_format == "json":
            complaint = generate_complaint_json(data)
        else:
            complaint = generate_complaint_markdown(data)

        logger.info("Complaint generated | type=%s | format=%s", scam_type, output_format)
        return {
            "scam_type": scam_type,
            "format": output_format,
            "complaint": complaint,
            "portal": "cybercrime.gov.in",
            "helpline": "1930",
        }


complaint_service = ComplaintService()