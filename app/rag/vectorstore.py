from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

from app.config import settings
from app.llm import get_embeddings

COLLECTION_NAME = "documents"

_client = QdrantClient(url=settings.qdrant_url, timeout=30)
_embeddings = get_embeddings()


def _ensure_collection(vector_size: int) -> None:
    if not _client.collection_exists(COLLECTION_NAME):
        _client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )


def upsert_chunks(document_id: str, filename: str, chunks: list[str]) -> None:
    vectors = _embeddings.embed_documents(chunks)
    _ensure_collection(vector_size=len(vectors[0]))

    points = [
        PointStruct(
            id=str(uuid4()),
            vector=vector,
            payload={
                "document_id": document_id,
                "filename": filename,
                "chunk_index": index,
                "text": chunk,
            },
        )
        for index, (chunk, vector) in enumerate(zip(chunks, vectors))
    ]
    _client.upsert(collection_name=COLLECTION_NAME, points=points)


def delete_document_chunks(document_id: str) -> None:
    if not _client.collection_exists(COLLECTION_NAME):
        return
    _client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=Filter(
            must=[FieldCondition(key="document_id", match=MatchValue(value=document_id))]
        ),
    )


def search(query: str, top_k: int = 4) -> list[dict]:
    if not _client.collection_exists(COLLECTION_NAME):
        return []

    query_vector = _embeddings.embed_query(query)
    results = _client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
    ).points

    return [
        {
            "text": point.payload["text"],
            "filename": point.payload["filename"],
            "document_id": point.payload["document_id"],
            "score": point.score,
        }
        for point in results
    ]
