"""Tests for the settings and CORS configuration."""

import pytest
from app.config.settings import Settings


def test_default_settings() -> None:
    s = Settings()
    assert s.app_version == "0.1.0"
    assert s.debug is False


def test_cors_origins_list_single() -> None:
    s = Settings(cors_origins="http://localhost:3000")
    assert s.cors_origins_list == ["http://localhost:3000"]


def test_cors_origins_list_multiple() -> None:
    s = Settings(cors_origins="http://localhost:3000,https://dpsp.vercel.app")
    assert len(s.cors_origins_list) == 2


def test_env_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEBUG", "true")
    s = Settings()
    assert s.debug is True
