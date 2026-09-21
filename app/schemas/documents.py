from datetime import datetime

from pydantic import BaseModel


class DocumentInfo(BaseModel):
    id: str
    filename: str
    content_type: str
    chunk_count: int
    ingested_at: datetime
