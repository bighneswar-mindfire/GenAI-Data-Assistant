import re

from langchain_ollama import ChatOllama

from app.config import settings
from app.sql_agent.db import get_schema_description

_llm = ChatOllama(model=settings.ollama_chat_model, base_url=settings.ollama_base_url, temperature=0)

SQL_PROMPT = """You are a PostgreSQL expert. Given the database schema below, write a single \
read-only SQL query that answers the question.

Schema:
{schema}

Rules:
- Output only the SQL query. No explanation, no markdown formatting, no code fences.
- Only use SELECT statements. Never use INSERT, UPDATE, DELETE, DROP, ALTER, or any other \
data-modifying statement.
- Only use the tables and columns listed in the schema above.
- If the question asks for a total, sum, count, or average, aggregate with SQL (SUM/COUNT/AVG) \
instead of returning raw rows.
- "Last month" means the previous full calendar month, not a rolling 30 days: use \
date_trunc('month', order_date) = date_trunc('month', CURRENT_DATE - INTERVAL '1 month').
- refund_amount is only meaningful (non-zero) on rows where status = 'refunded'; filter on \
status = 'refunded' when asked about refunds.
- The question may also ask about something that is NOT in this database (e.g. a policy or \
procedure). Ignore that part entirely: do not invent columns or computations to represent it. \
Never create a column named after a non-numeric concept like "policy" or "procedure" — those \
words do not correspond to any column or calculation. Just answer the numeric/data part.

Question: {question}

SQL query:"""

RETRY_PROMPT = """Your previous PostgreSQL query failed. Fix it.

Schema:
{schema}

Question: {question}

Previous query:
{previous_sql}

Error:
{error}

Reminder: only compute the numeric/data part of the question. Never create a column named after \
a non-numeric concept like "policy" or "procedure" — those words do not correspond to any column \
or calculation.

Output only the corrected SQL query. No explanation, no markdown formatting, no code fences."""


def generate_sql(question: str) -> str:
    schema = get_schema_description()
    prompt = SQL_PROMPT.format(schema=schema, question=question)
    response = _llm.invoke(prompt)
    return _strip_code_fences(response.content.strip())


def regenerate_sql(question: str, previous_sql: str, error: str) -> str:
    schema = get_schema_description()
    prompt = RETRY_PROMPT.format(schema=schema, question=question, previous_sql=previous_sql, error=error)
    response = _llm.invoke(prompt)
    return _strip_code_fences(response.content.strip())


def _strip_code_fences(text: str) -> str:
    match = re.search(r"```(?:sql)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else text
