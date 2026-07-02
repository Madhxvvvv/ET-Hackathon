"""
response_pipeline.py
End-to-end response pipeline.
Language Detection → Scam Classification → Retrieval → Formatting → Translation
"""

from __future__ import annotations

import time
from typing import Optional

from configs.config import get_logger
from src.agents.digital_arrest_agent import analyze
from src.agents.response_models import AgentResponse
from src.utils.formatter import format_response_dict, format_response_markdown
from src.utils.language_detector import detect_language
from src.utils.translator import translate_response

logger = get_logger(__name__)


def run_pipeline(
    user_message: str,
    session_id: Optional[str] = None,
    is_transcript: bool = False,
    output_format: str = "markdown",
) -> dict:
    """
    Full pipeline: detect language → analyze → format → translate.

    Args:
        user_message: User input text
        session_id: Optional session ID for context
        is_transcript: True if input is a full call transcript
        output_format: 'markdown' or 'dict'

    Returns:
        Dict with formatted response and metadata
    """
    start = time.time()
    logger.info("Pipeline started | session=%s | length=%d", session_id, len(user_message))

    # Step 1 — language detection
    language = detect_language(user_message)
    logger.info("Language detected: %s", language)

    # Step 2 — agent analysis
    response: AgentResponse = analyze(user_message, is_transcript=is_transcript)

    # Step 3 — format
    if output_format == "markdown":
        formatted = format_response_markdown(response)
    else:
        formatted = format_response_dict(response)

    # Step 4 — translate if needed
    if language != "en" and isinstance(formatted, str):
        formatted = translate_response(formatted, language)

    elapsed = time.time() - start
    logger.info("Pipeline completed in %.2fs | risk=%s", elapsed, response.risk_level.value)

    return {
        "session_id": session_id,
        "language": language,
        "risk_level": response.risk_level.value,
        "is_scam": response.is_scam,
        "response": formatted,
        "latency_seconds": round(elapsed, 3),
    }