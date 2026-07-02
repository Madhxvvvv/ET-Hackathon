"""
session_service.py
Service layer for session management.
Clean interface for future FastAPI integration.
"""

from __future__ import annotations

from typing import Optional

from configs.config import get_logger
from src.session_manager import session_manager

logger = get_logger(__name__)


class SessionService:
    """Handles session lifecycle operations."""

    def create(self, language: str = "en") -> dict:
        """Create a new session."""
        session = session_manager.create_session(language=language)
        logger.info("Session created: %s", session.session_id)
        return {
            "session_id": session.session_id,
            "language": session.language,
            "created_at": session.created_at.isoformat(),
        }

    def get(self, session_id: str) -> dict:
        """Get session details."""
        session = session_manager.get_session(session_id)
        if not session:
            return {"error": "Session not found or expired"}
        return {
            "session_id": session.session_id,
            "language": session.language,
            "created_at": session.created_at.isoformat(),
            "last_active": session.last_active.isoformat(),
            "message_count": len(session.messages),
            "is_expired": session.is_expired(),
        }

    def delete(self, session_id: str) -> dict:
        """Delete a session."""
        session_manager.delete_session(session_id)
        return {"session_id": session_id, "deleted": True}

    def cleanup(self) -> dict:
        """Clean up all expired sessions."""
        count = session_manager.cleanup_expired()
        return {
            "cleaned_up": count,
            "active_sessions": session_manager.active_session_count(),
        }

    def update_language(self, session_id: str, language: str) -> dict:
        """Update language preference for a session."""
        session = session_manager.get_session(session_id)
        if not session:
            return {"error": "Session not found or expired"}
        session.language = language
        logger.info("Session %s language updated to %s", session_id, language)
        return {
            "session_id": session_id,
            "language": language,
            "updated": True,
        }


session_service = SessionService()