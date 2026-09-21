from fastapi import FastAPI

from app.routers import documents, health

app = FastAPI(
    title="Local GenAI Data Assistant",
    description="Chat with documents (RAG) and SQL data, fully local.",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(documents.router)
