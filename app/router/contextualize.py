from langchain_ollama import ChatOllama

from app.config import settings

_llm = ChatOllama(model=settings.ollama_chat_model, base_url=settings.ollama_base_url, temperature=0)

CONTEXTUALIZE_PROMPT = """Given the conversation history and a follow-up question, rewrite the \
follow-up question as a standalone question that includes any necessary context from the \
history (e.g. resolve pronouns like "it" or "that", or fill in an implied subject). If the \
follow-up question is already standalone and doesn't depend on the history, return it \
unchanged. Output only the rewritten question, nothing else.

Conversation history:
{history}

Follow-up question: {question}

Standalone question:"""


def contextualize(question: str, history: list[dict]) -> str:
    if not history:
        return question

    history_text = "\n".join(f"{turn['role']}: {turn['content']}" for turn in history)
    prompt = CONTEXTUALIZE_PROMPT.format(history=history_text, question=question)
    response = _llm.invoke(prompt)
    return response.content.strip()
