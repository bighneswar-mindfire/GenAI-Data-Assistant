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

Question: {question}

SQL query:"""


def generate_sql(question: str) -> str:
    schema = get_schema_description()
    prompt = SQL_PROMPT.format(schema=schema, question=question)
    response = _llm.invoke(prompt)
    return _strip_code_fences(response.content.strip())


def _strip_code_fences(text: str) -> str:
    match = re.search(r"```(?:sql)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else text
