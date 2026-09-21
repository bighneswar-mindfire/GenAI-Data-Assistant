from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.config import settings
from app.rag.chunking import chunk_text
from app.rag.loaders import load_text
from app.rag.vectorstore import delete_document_chunks, upsert_chunks
from app.schemas.documents import DocumentInfo
from app.store import documents

router = APIRouter(prefix="/documents", tags=["documents"])

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}


@router.get("", response_model=list[DocumentInfo])
def list_documents():
    return list(documents.values())


@router.post("/ingest", response_model=DocumentInfo)
async def ingest_document(file: UploadFile = File(...)):
    extension = Path(file.filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{extension}'. Allowed: {sorted(ALLOWED_EXTENSIONS)}",
        )

    documents_dir = Path(settings.documents_dir)
    documents_dir.mkdir(parents=True, exist_ok=True)

    doc_id = str(uuid4())
    content = await file.read()
    dest_path = documents_dir / f"{doc_id}{extension}"
    dest_path.write_bytes(content)

    text = load_text(dest_path)
    chunks = chunk_text(text)

    try:
        upsert_chunks(document_id=doc_id, filename=file.filename, chunks=chunks)
    except Exception as exc:
        dest_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Embedding service unavailable: {exc}",
        ) from exc

    info = DocumentInfo(
        id=doc_id,
        filename=file.filename,
        content_type=file.content_type or "application/octet-stream",
        chunk_count=len(chunks),
        ingested_at=datetime.now(timezone.utc),
    )
    documents[doc_id] = info
    return info


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: str):
    if document_id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")

    documents_dir = Path(settings.documents_dir)
    for path in documents_dir.glob(f"{document_id}.*"):
        path.unlink()

    delete_document_chunks(document_id)
    del documents[document_id]
