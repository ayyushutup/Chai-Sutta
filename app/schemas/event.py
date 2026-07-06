"""Event-related Pydantic schemas."""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import GeoPoint


class EventCreate(BaseModel):
    """Schema for creating a new event."""
    title: str = Field(..., min_length=1, max_length=500)
    description: str | None = None
    category: str = Field(..., max_length=50)
    city_id: UUID
    zone_id: UUID | None = None
    location: GeoPoint | None = None
    starts_at: datetime
    ends_at: datetime | None = None


class EventResponse(BaseModel):
    """Schema for event data in API responses."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None = None
    category: str
    zone_id: UUID | None = None
    city_id: UUID
    starts_at: datetime
    ends_at: datetime | None = None
    source: str
    created_at: datetime
