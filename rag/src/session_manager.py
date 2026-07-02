"""
session_manager.py
Manages conversation sessions with history, metadata, and expiration.
Future-ready for Redis integration.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional

from configs.config import get_logger

logger = get_logger(__name__)

SESSION_TIMEOUT_MINUTES = 30


@dataclass
class Message:
    role: str  # "user" | "assistant"
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    language: str = "en"


@dataclass
class Session:
    session_id: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_active: datetime = field(default_factory=datetime.utcnow)
    language: str = "en"
    messages: list[Message] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def is_expired(self, timeout_minutes: int = SESSION_TIMEOUT_MINUTES) -> bool:
        return datetime.utcnow() > self.last_active + timedelta(minutes=timeout_minutes)

    def add_message(self, role: str, content: str, language: str = "en") -> None:
        self.messages.append(Message(role=role, content=content, language=language))
        self.last_active = datetime.utcnow()

    def get_history(self, last_n: int = 10) -> list[dict]:
        return [
            {
                "role": m.role,
                "content": m.content,
                "timestamp": m.timestamp.isoformat(),
                "language": m.language,
            }
            for m in self.messages[-last_n:]
        ]


class SessionManager:
    """
    In-memory session manager.
    Future-ready for Redis by replacing _sessions dict
    with Redis client calls.
    """

    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}

    def create_session(self, language: str = "en") -> Session:
        session_id = str(uuid.uuid4())
        session = Session(session_id=session_id, language=language)
        self._sessions[session_id] = session
        logger.info("Created session: %s", session_id)
        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        session = self._sessions.get(session_id)
        if not session:
            logger.warning("Session not found: %s", session_id)
            return None
        if session.is_expired():
            logger.info("Session expired: %s", session_id)
            self.delete_session(session_id)
            return None
        return session

    def get_or_create(self, session_id: Optional[str], language: str = "en") -> Session:
        if session_id:
            session = self.get_session(session_id)
            if session:
                return session
        return self.create_session(language=language)

    def delete_session(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)
        logger.info("Deleted session: %s", session_id)

    def cleanup_expired(self) -> int:
        expired = [
            sid for sid, s in self._sessions.items() if s.is_expired()
        ]
        for sid in expired:
            self.delete_session(sid)
        logger.info("Cleaned up %d expired sessions", len(expired))
        return len(expired)

    def active_session_count(self) -> int:
        return len(self._sessions)


# Singleton instance
session_manager = SessionManager()