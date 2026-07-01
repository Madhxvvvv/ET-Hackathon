"""Tests for the /api/v1/fraud-network endpoints."""

from fastapi.testclient import TestClient


def test_graph_returns_501(client: TestClient) -> None:
    response = client.get("/api/v1/fraud-network/graph")
    assert response.status_code == 501


def test_node_detail_returns_501(client: TestClient) -> None:
    response = client.get("/api/v1/fraud-network/nodes/abc123")
    assert response.status_code == 501


def test_graph_endpoint_in_openapi(client: TestClient) -> None:
    schema = client.get("/openapi.json").json()
    assert "/api/v1/fraud-network/graph" in schema["paths"]


def test_node_endpoint_in_openapi(client: TestClient) -> None:
    schema = client.get("/openapi.json").json()
    assert "/api/v1/fraud-network/nodes/{node_id}" in schema["paths"]
