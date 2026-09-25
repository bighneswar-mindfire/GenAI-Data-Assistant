from app.llm import get_chat_llm

_llm = get_chat_llm()

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
