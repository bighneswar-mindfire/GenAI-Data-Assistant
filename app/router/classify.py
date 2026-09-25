from typing import Literal

from pydantic import BaseModel, Field

from app.llm import get_chat_llm

Route = Literal["document", "sql", "combined"]


class RouteDecision(BaseModel):
    route: Route = Field(description="Which system should answer the question")


_llm = get_chat_llm()
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
