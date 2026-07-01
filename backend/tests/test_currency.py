"""Tests for the /api/v1/currency endpoints."""

import io
from fastapi.testclient import TestClient


def test_detect_no_file_returns_422(client: TestClient) -> None:
    response = client.post("/api/v1/currency/detect")
    assert response.status_code == 422


def test_detect_non_image_returns_422(client: TestClient) -> None:
    response = client.post(
        "/api/v1/currency/detect",
        files={"file": ("doc.txt", io.BytesIO(b"hello"), "text/plain")},
    )
    assert response.status_code == 422


def test_detect_image_returns_501(client: TestClient) -> None:
    # Day 2: this will return 200 with a prediction.
    response = client.post(
        "/api/v1/currency/detect",
        files={"file": ("note.jpg", io.BytesIO(b"\xff\xd8\xff"), "image/jpeg")},
    )
    assert response.status_code == 501


def test_detect_endpoint_in_openapi(client: TestClient) -> None:
    schema = client.get("/openapi.json").json()
    assert "/api/v1/currency/detect" in schema["paths"]
