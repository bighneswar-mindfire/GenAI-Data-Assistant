from sqlalchemy import text

from app.sql_agent.db import engine


STATEMENT_TIMEOUT_MS = 10_000


def execute_select(sql: str) -> list[dict]:
    with engine.connect() as conn:
        conn.execute(text("SET TRANSACTION READ ONLY"))
        conn.execute(text(f"SET LOCAL statement_timeout = {STATEMENT_TIMEOUT_MS}"))
        result = conn.execute(text(sql))
        columns = result.keys()
        return [dict(zip(columns, row)) for row in result.fetchall()]
