from uuid import uuid4

from fastapi import APIRouter

from app.router.graph import route_question
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    session_id = request.session_id or str(uuid4())
    result = route_question(request.message)
    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"],
        session_id=session_id,
    )
