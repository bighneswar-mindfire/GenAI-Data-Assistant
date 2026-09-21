from fastapi import APIRouter

from app.schemas.documents import DocumentInfo
from app.store import documents

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("", response_model=list[DocumentInfo])
def list_documents():
    return list(documents.values())
