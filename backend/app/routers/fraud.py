"""Fraud network router — Neo4j graph query stubs."""

import logging
from fastapi import APIRouter, HTTPException

from app.schemas.fraud import GraphResponse, NodeDetail

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/fraud-network", tags=["fraud-network"])


@router.get("/graph", response_model=GraphResponse)
async def get_graph() -> GraphResponse:
    """Returns all fraud network nodes and edges from Neo4j.

    Day 2: query Neo4j via the database layer.
    """
    logger.info("Fraud graph request received.")
    raise HTTPException(status_code=501, detail="Neo4j integration not yet available (Day 2).")


@router.get("/nodes/{node_id}", response_model=NodeDetail)
async def get_node(node_id: str) -> NodeDetail:
    """Returns details for a single fraud network node."""
    logger.info("Node detail request: %s", node_id)
    raise HTTPException(status_code=501, detail="Neo4j integration not yet available (Day 2).")
