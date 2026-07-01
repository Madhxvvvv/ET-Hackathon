"""Tests for the /api/v1/scam-shield endpoints."""

from fastapi.testclient import TestClient


def test_query_returns_501(client: TestClient) -> None:
    response = client.post(
        "/api/v1/scam-shield/query",
        json={"question": "Is digital arrest legal in India?"},
    )
    assert response.status_code == 501


def test_query_too_short_returns_422(client: TestClient) -> None:
    response = client.post(
        "/api/v1/scam-shield/query",
        json={"question": "Hi"},
    )
    assert response.status_code == 422


def test_query_missing_body_returns_422(client: TestClient) -> None:
    response = client.post("/api/v1/scam-shield/query", json={})
    assert response.status_code == 422


def test_query_endpoint_in_openapi(client: TestClient) -> None:
    schema = client.get("/openapi.json").json()
    assert "/api/v1/scam-shield/query" in schema["paths"]
