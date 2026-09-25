import httpx
from fastapi import APIRouter
from sqlalchemy import text

from app.config import settings
from app.sql_agent.db import engine

router = APIRouter(tags=["health"])


def _check_postgres() -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


def _check_qdrant() -> bool:
    try:
        httpx.get(f"{settings.qdrant_url}/collections", timeout=3)
        return True
    except Exception:
        return False


def _check_ollama() -> bool:
    try:
        httpx.get(f"{settings.ollama_base_url}/api/tags", timeout=3)
        return True
    except Exception:
        return False


@router.get("/health")
def health_check():
    services = {
        "postgres": "ok" if _check_postgres() else "unreachable",
        "qdrant": "ok" if _check_qdrant() else "unreachable",
        "ollama": "ok" if _check_ollama() else "unreachable",
    }
    status = "ok" if all(v == "ok" for v in services.values()) else "degraded"
    return {"status": status, "services": services}
