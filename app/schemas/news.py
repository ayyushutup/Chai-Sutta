"""News-related Pydantic schemas."""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import PaginationParams


class NewsResponse(BaseModel):
    """Schema for news article data in API responses."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    summary: str | None = None
    source_url: str
    source_name: str
    category: str
    importance_score: int
    zone_id: UUID | None = None
    city_id: UUID
    published_at: datetime | None = None
    created_at: datetime
    ai_metadata: dict | None = None


class NewsFeedParams(BaseModel):
    """Parameters for querying the news feed."""
    city_id: UUID
    zone_id: UUID | None = None
    category: str | None = None
    pagination: PaginationParams = Field(default_factory=PaginationParams)
