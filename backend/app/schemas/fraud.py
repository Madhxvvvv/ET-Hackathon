"""Pydantic schemas for the fraud network endpoints."""

from pydantic import BaseModel, Field


class FraudNode(BaseModel):
    id: str
    label: str
    properties: dict[str, str | int | float | bool] = Field(default_factory=dict)


class FraudEdge(BaseModel):
    source: str
    target: str
    relationship: str


class GraphResponse(BaseModel):
    nodes: list[FraudNode] = Field(default_factory=list)
    edges: list[FraudEdge] = Field(default_factory=list)
    total_nodes: int = 0
    total_edges: int = 0


class NodeDetail(BaseModel):
    node: FraudNode
    connected_edges: list[FraudEdge] = Field(default_factory=list)
