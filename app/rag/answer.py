from app.llm import get_chat_llm
from app.rag.vectorstore import search

_llm = get_chat_llm()

MIN_RELEVANCE_SCORE = 0.5
RELEVANCE_MARGIN = 0.15

RAG_PROMPT = """Answer the question using only the context below. The question may ask about \
something the context doesn't cover (e.g. live data or numbers from a database) — in that case, \
give the full, specific answer (not just a vague reference) for the part the context does cover, \
and simply omit the part it doesn't, without apologizing or mentioning what's missing. Only say \
you don't know if NONE of the question is answerable from the context.

Context:
{context}

Question: {question}

Answer:"""


def answer_question(question: str, top_k: int = 4) -> dict:
    all_hits = search(question, top_k=top_k)
    top_score = all_hits[0]["score"] if all_hits else 0
    cutoff = max(MIN_RELEVANCE_SCORE, top_score - RELEVANCE_MARGIN)
    hits = [h for h in all_hits if h["score"] >= cutoff]
    if not hits:
        return {"answer": "I don't have any relevant documents to answer that.", "sources": []}

    context = "\n\n".join(f"[{hit['filename']}] {hit['text']}" for hit in hits)
    prompt = RAG_PROMPT.format(context=context, question=question)
    response = _llm.invoke(prompt)
    sources = sorted({hit["filename"] for hit in hits})
    return {"answer": response.content, "sources": sources}
