import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routers import chat, documents, health

logger = logging.getLogger("app")

app = FastAPI(
    title="Local GenAI Data Assistant",
    description="Chat with documents (RAG) and SQL data, fully local.",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(documents.router)
app.include_router(chat.router)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
