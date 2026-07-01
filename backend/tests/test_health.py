"""Tests for the /health endpoint and application metadata."""

from fastapi.testclient import TestClient


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200


def test_health_body(client: TestClient) -> None:
    data = client.get("/health").json()
    assert data["status"] == "ok"
    assert "version" in data


def test_docs_available(client: TestClient) -> None:
    assert client.get("/docs").status_code == 200


def test_openapi_schema(client: TestClient) -> None:
    schema = client.get("/openapi.json").json()
    assert schema["info"]["title"] == "Digital Public Safety Platform"


def test_unknown_route_returns_404(client: TestClient) -> None:
    assert client.get("/does-not-exist").status_code == 404
