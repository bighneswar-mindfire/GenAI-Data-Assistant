from langchain_ollama import ChatOllama, OllamaEmbeddings

from app.config import settings

REQUEST_TIMEOUT_SECONDS = 60


def get_chat_llm(temperature: float = 0) -> ChatOllama:
    return ChatOllama(
        model=settings.ollama_chat_model,
        base_url=settings.ollama_base_url,
        temperature=temperature,
        client_kwargs={"timeout": REQUEST_TIMEOUT_SECONDS},
    )


def get_embeddings() -> OllamaEmbeddings:
    return OllamaEmbeddings(
        model=settings.ollama_embed_model,
        base_url=settings.ollama_base_url,
        client_kwargs={"timeout": REQUEST_TIMEOUT_SECONDS},
    )
