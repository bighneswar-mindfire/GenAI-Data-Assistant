from uuid import uuid4

from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    session_id = request.session_id or str(uuid4())
    return ChatResponse(
        answer="Chat is not wired up yet.",
        sources=[],
        session_id=session_id,
    )
