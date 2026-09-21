from langchain_ollama import ChatOllama

from app.config import settings
from app.rag.vectorstore import search

_llm = ChatOllama(model=settings.ollama_chat_model, base_url=settings.ollama_base_url, temperature=0)

MIN_RELEVANCE_SCORE = 0.6

RAG_PROMPT = """Answer the question using only the context below. \
If the answer isn't in the context, say you don't know.

Context:
{context}

Question: {question}

Answer:"""


def answer_question(question: str, top_k: int = 4) -> dict:
    hits = [h for h in search(question, top_k=top_k) if h["score"] >= MIN_RELEVANCE_SCORE]
    if not hits:
        return {"answer": "I don't have any relevant documents to answer that.", "sources": []}

    context = "\n\n".join(f"[{hit['filename']}] {hit['text']}" for hit in hits)
    prompt = RAG_PROMPT.format(context=context, question=question)
    response = _llm.invoke(prompt)
    sources = sorted({hit["filename"] for hit in hits})
    return {"answer": response.content, "sources": sources}
