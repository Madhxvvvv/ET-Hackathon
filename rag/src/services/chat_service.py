"""
chat_service.py
Service layer for chat interactions.
Clean interface for future FastAPI integration.
"""

from __future__ import annotations

from typing import Optional

from configs.config import get_logger
from src.response_pipeline import run_pipeline
from src.session_manager import session_manager
from src.utils.language_detector import detect_language
from src.utils.translator import get_language_greeting

logger = get_logger(__name__)


class ChatService:
    """Handles chat interactions with session awareness."""

    def chat(
        self,
        message: str,
        session_id: Optional[str] = None,
        is_transcript: bool = False,
        output_format: str = "markdown",
    ) -> dict:
        """
        Process a chat message and return a structured response.

        Args:
            message: User message
            session_id: Optional session ID
            is_transcript: True if message is a full call transcript
            output_format: 'markdown' or 'dict'

        Returns:
            Response dict with risk assessment and formatted output
        """
        language = detect_language(message)
        session = session_manager.get_or_create(session_id, language=language)

        # add user message to session
        session.add_message("user", message, language=language)

        # run pipeline
        result = run_pipeline(
            user_message=message,
            session_id=session.session_id,
            is_transcript=is_transcript,
            output_format=output_format,
        )

        # add assistant response to session
        session.add_message(
            "assistant",
            str(result.get("response", "")),
            language=language,
        )

        result["session_id"] = session.session_id
        result["conversation_length"] = len(session.messages)
        logger.info(
            "Chat processed | session=%s | risk=%s",
            session.session_id,
            result.get("risk_level"),
        )
        return result

    def get_greeting(self, session_id: Optional[str] = None, language: str = "en") -> dict:
        """Return a greeting message in the detected language."""
        session = session_manager.get_or_create(session_id, language=language)
        greeting = get_language_greeting(language)
        session.add_message("assistant", greeting, language=language)
        return {
            "session_id": session.session_id,
            "language": language,
            "response": greeting,
        }

    def get_history(self, session_id: str) -> dict:
        """Return conversation history for a session."""
        session = session_manager.get_session(session_id)
        if not session:
            return {"error": "Session not found or expired"}
        return {
            "session_id": session_id,
            "language": session.language,
            "messages": session.get_history(),
            "message_count": len(session.messages),
        }


chat_service = ChatService()