"""Centralised settings — all values overridable via environment variables."""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Server
    app_name: str = "Digital Public Safety Platform"
    app_version: str = "0.1.0"
    debug: bool = False

    # CORS — comma-separated origins
    cors_origins: str = "http://localhost:3000"

    # Neo4j
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "password"

    # ML service (Day 2)
    ml_service_url: str = "http://localhost:8001"

    # RAG service (Day 2)
    rag_service_url: str = "http://localhost:8002"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
