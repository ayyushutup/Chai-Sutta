"""Search-related Pydantic schemas."""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import GeoPoint, TimePeriod


class SearchRequest(BaseModel):
    """Schema for search query parameters."""
    query: str = Field(..., min_length=1, max_length=500)
    category: str | None = None
    city_id: UUID | None = None
    zone_id: UUID | None = None
    location: GeoPoint | None = None
    radius_km: float = Field(5.0, ge=0.1, le=50.0)
    time_period: TimePeriod | None = None


class SearchResultItem(BaseModel):
    """Schema for a single search result item."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    type: str
    title: str
    snippet: str
    category: str | None = None
    distance_km: float | None = None
    relevance_score: float
    created_at: datetime


class SearchResponse(BaseModel):
    """Schema for search results response."""
    results: list[SearchResultItem]
    total: int
    query: str
