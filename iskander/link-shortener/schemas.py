from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field


class URLCreate(BaseModel):
    url: HttpUrl = Field(..., description="Оригинальный URL для сокращения")


class URLInfo(BaseModel):
    code: str
    short_url: str
    original_url: str
    created_at: datetime
    clicks: int

    class Config:
        from_attributes = True