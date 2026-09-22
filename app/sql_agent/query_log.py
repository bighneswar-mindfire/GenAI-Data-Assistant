import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("sql_agent")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.FileHandler(LOG_DIR / "sql_queries.log", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s | %(message)s"))
    logger.addHandler(handler)


def log_query(question: str, sql: str, row_count: int = 0, error: str | None = None) -> None:
    if error:
        logger.info("QUESTION=%r SQL=%r ERROR=%r", question, sql, error)
    else:
        logger.info("QUESTION=%r SQL=%r ROWS=%d", question, sql, row_count)
