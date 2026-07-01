"""
complaint_response.py
Pydantic schemas for complaint generation response contracts.
Ready for FastAPI integration on Day 4.
"""

from __future__ import annotations

from typing import Union
from pydantic import BaseModel


class ComplaintResponse(BaseModel):
    """Schema for complaint generation responses."""

    scam_type: str
    format: str
    complaint: Union[str, dict]
    portal: str = "cybercrime.gov.in"
    helpline: str = "1930"