import json

from langchain_ollama import ChatOllama

from app.config import settings
from app.sql_agent.executor import execute_select
from app.sql_agent.generate import generate_sql, regenerate_sql
from app.sql_agent.query_log import log_query
from app.sql_agent.validate import validate_select_only

_llm = ChatOllama(model=settings.ollama_chat_model, base_url=settings.ollama_base_url, temperature=0)

ANSWER_PROMPT = """Answer the user's question using only the query result data below. \
Do not invent or alter any numbers.

Question: {question}

Query result (JSON rows):
{rows}

Answer concisely in natural language."""


def _validate_and_execute(sql: str) -> tuple[str, list[dict]]:
    validated_sql = validate_select_only(sql)
    rows = execute_select(validated_sql)
    return validated_sql, rows


def answer_sql_question(question: str) -> dict:
    sql = generate_sql(question)

    try:
        validated_sql, rows = _validate_and_execute(sql)
    except Exception as first_error:
        sql = regenerate_sql(question, previous_sql=sql, error=str(first_error))
        try:
            validated_sql, rows = _validate_and_execute(sql)
        except Exception as second_error:
            log_query(question, sql, error=str(second_error))
            raise

    log_query(question, validated_sql, row_count=len(rows))

    prompt = ANSWER_PROMPT.format(question=question, rows=json.dumps(rows, default=str))
    response = _llm.invoke(prompt)

    return {"answer": response.content, "sql": validated_sql, "rows": rows}
