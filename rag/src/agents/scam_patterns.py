"""
scam_patterns.py
Defines scam pattern keyword sets used by the ScamPatternDetector tool.
Keeping patterns in a separate file makes them easy to update without
touching agent logic.
"""

from __future__ import annotations

SCAM_PATTERNS: dict[str, list[str]] = {
    "police_impersonation": [
        "police", "officer", "thana", "FIR", "arrest warrant",
        "daroga", "inspector", "constable", "IPS",
    ],
    "cbi_impersonation": [
        "CBI", "Central Bureau", "investigation", "federal agent",
        "CBI officer", "CBI headquarters",
    ],
    "rbi_impersonation": [
        "RBI", "Reserve Bank", "RBI officer", "banking regulation",
        "RBI verification", "RBI notice",
    ],
    "digital_arrest": [
        "digital arrest", "you are arrested", "aap arrested hain",
        "digital custody", "online arrest", "virtual arrest",
        "ghar pe rehna hoga", "bahar mat jaana",
    ],
    "kyc_scam": [
        "KYC", "KYC expired", "KYC update", "KYC pending",
        "KYC verification", "KYC block", "KYC freeze",
    ],
    "upi_fraud": [
        "UPI", "scan QR", "QR code", "receive money", "payment link",
        "UPI ID", "Google Pay", "PhonePe", "paisa aayega",
    ],
    "otp_fraud": [
        "OTP", "one time password", "share OTP", "OTP batao",
        "OTP verify", "OTP send karo",
    ],
    "account_freeze": [
        "account freeze", "account block", "account suspend",
        "account band", "khata freeze", "bank account freeze",
    ],
    "money_laundering": [
        "money laundering", "hawala", "illegal transaction",
        "black money", "suspicious transaction", "kala paisa",
    ],
    "remote_access": [
        "AnyDesk", "TeamViewer", "remote access", "screen share",
        "install app", "download app", "apna phone do",
    ],
    "courier_scam": [
        "parcel", "courier", "package", "customs", "drug parcel",
        "illegal parcel", "DHL", "FedEx notice",
    ],
    "investment_scam": [
        "guaranteed returns", "double money", "invest now",
        "high returns", "trading profit", "stock tip",
    ],
}

EMERGENCY_CONTACTS: dict[str, str] = {
    "cybercrime_helpline": "1930",
    "cybercrime_portal": "cybercrime.gov.in",
    "police_emergency": "100",
    "women_helpline": "1091",
    "senior_citizen_helpline": "14567",
}

SAFE_KEYWORDS: list[str] = [
    "how are you", "weather", "recipe", "movie", "cricket",
    "normal banking", "balance enquiry", "mini statement",
    "account opening", "loan enquiry", "credit card bill",
]