from sqlalchemy import text

from app.sql_agent.db import engine


def execute_select(sql: str) -> list[dict]:
    with engine.connect() as conn:
        conn.execute(text("SET TRANSACTION READ ONLY"))
        result = conn.execute(text(sql))
        columns = result.keys()
        return [dict(zip(columns, row)) for row in result.fetchall()]
