from pydantic import BaseModel
from datetime import datetime


class DocumentOut(BaseModel):
    id: int
    filename: str
    content_type: str
    size_bytes: int
    tags: str
    download_url: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
