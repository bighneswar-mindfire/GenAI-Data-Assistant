from typing import Literal

from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

from app.config import settings

Route = Literal["document", "sql", "combined"]


class RouteDecision(BaseModel):
    route: Route = Field(description="Which system should answer the question")


_llm = ChatOllama(model=settings.ollama_chat_model, base_url=settings.ollama_base_url, temperature=0)
_classifier = _llm.with_structured_output(RouteDecision, method="function_calling")

CLASSIFY_PROMPT = """Classify the question below into exactly one category:

- "document": answerable from company policy documents (e.g. leave, refund, remote work, \
expense, onboarding policies).
- "sql": asks about structured business data stored in a database (customers, products, \
orders, revenue, refund amounts, counts, etc).
- "combined": requires BOTH a policy explanation AND database numbers to fully answer.

Question: {question}"""


def classify(question: str) -> Route:
    prompt = CLASSIFY_PROMPT.format(question=question)
    decision: RouteDecision = _classifier.invoke(prompt)
    return decision.route
