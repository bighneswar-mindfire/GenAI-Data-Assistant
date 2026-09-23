from uuid import uuid4

from fastapi import APIRouter

from app.conversation import append_turn, get_history
from app.router.graph import route_question
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    session_id = request.session_id or str(uuid4())
    history = get_history(session_id)

    result = route_question(request.message, history=history)

    append_turn(session_id, "user", request.message)
    append_turn(session_id, "assistant", result["answer"])

    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"],
        session_id=session_id,
    )
