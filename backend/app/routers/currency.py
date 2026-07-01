"""Currency detection router — ML inference endpoint stubs."""

import logging
from fastapi import APIRouter, File, UploadFile, HTTPException

from app.schemas.currency import DetectResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/currency", tags=["currency"])


@router.post("/detect", response_model=DetectResponse)
async def detect_currency(file: UploadFile = File(...)) -> DetectResponse:
    """Accepts an image upload and returns a genuine/counterfeit classification.

    Day 2: forward image bytes to the ML module inference endpoint.
    """
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=422, detail="File must be an image.")

    logger.info("Currency detection request received: %s", file.filename)
    raise HTTPException(status_code=501, detail="ML inference not yet integrated (Day 2).")
