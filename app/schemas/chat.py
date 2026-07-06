"""Chat-related Pydantic schemas."""
from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import GeoPoint


class ChatRequest(BaseModel):
    """Schema for chat message request."""
    message: str = Field(..., min_length=1, max_length=2000)
    city_id: UUID | None = None
    zone_id: UUID | None = None
    location: GeoPoint | None = None


class ChatResponse(BaseModel):
    """Schema for chat message response."""
    reply: str
    sources: list[dict] = Field(default_factory=list)
    suggested_followups: list[str] = Field(default_factory=list)
