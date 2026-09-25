import httpx
import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app
from app.sql_agent.db import engine


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


def _http_reachable(url: str) -> bool:
    try:
        httpx.get(url, timeout=2)
        return True
    except Exception:
        return False


def _postgres_reachable() -> bool:
    try:
        with engine.connect():
            return True
    except Exception:
        return False


@pytest.fixture(scope="session")
def live_services_available():
    return (
        _http_reachable(f"{settings.ollama_base_url}/api/tags")
        and _http_reachable(f"{settings.qdrant_url}/collections")
        and _postgres_reachable()
    )
