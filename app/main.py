from fastapi import FastAPI

app = FastAPI(
    title="Local GenAI Data Assistant",
    description="Chat with documents (RAG) and SQL data, fully local.",
    version="0.1.0",
)
