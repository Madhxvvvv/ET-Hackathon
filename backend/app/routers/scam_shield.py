"""Scam Shield router — RAG query endpoint stubs."""

import logging
from fastapi import APIRouter, HTTPException

from app.schemas.scam_shield import QueryRequest, QueryResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/scam-shield", tags=["scam-shield"])


@router.post("/query", response_model=QueryResponse)
async def query_scam_shield(body: QueryRequest) -> QueryResponse:
    """Accepts a natural-language question and returns a RAG-grounded answer.

    Day 2: call the RAG module's retrieve() function and pass chunks to an LLM.
    """
    logger.info("Scam Shield query: %s", body.question[:80])
    raise HTTPException(status_code=501, detail="RAG integration not yet available (Day 2).")
