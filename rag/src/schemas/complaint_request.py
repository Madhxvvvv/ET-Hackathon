"""
complaint_request.py
Pydantic schemas for complaint generation request contracts.
Ready for FastAPI integration on Day 4.
"""

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


VALID_SCAM_TYPES = [
    "Digital Arrest Scam",
    "OTP Fraud",
    "UPI Fraud",
    "Fake Police Call",
    "KYC Scam",
    "Bank Fraud",
    "QR Code Scam",
    "Courier Scam",
    "Investment Scam",
    "SIM Swap",
    "Remote Access Scam",
    "Other",
]


class ComplaintRequest(BaseModel):
    """Schema for complaint generation requests."""

    scam_type: str = Field(
        ...,
        description=f"Type of scam. Options: {', '.join(VALID_SCAM_TYPES)}"
    )
    incident_description: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Detailed description of what happened"
    )
    victim_name: str = Field(default="Not Provided")
    victim_phone: str = Field(default="Not Provided")
    victim_email: str = Field(default="Not Provided")
    money_lost: float = Field(default=0.0, ge=0.0)
    suspect_phone: str = Field(default="Not Provided")
    suspect_account: str = Field(default="Not Provided")
    bank_name: str = Field(default="Not Provided")
    transaction_id: str = Field(default="Not Provided")
    evidence_available: list[str] = Field(default_factory=list)
    output_format: str = Field(
        default="markdown",
        description="Output format. Options: markdown, json"
    )