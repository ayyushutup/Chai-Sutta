"""Community report Pydantic schemas."""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import GeoPoint, SeverityEnum


class ReportCreate(BaseModel):
    """Schema for creating a new community report."""
    content: str = Field(..., min_length=1)
    category: str = Field(..., max_length=50)
    severity: SeverityEnum = SeverityEnum.LOW
    city_id: UUID
    location: GeoPoint | None = None
    media_type: str = "none"


class ReportResponse(BaseModel):
    """Schema for community report data in API responses."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    content: str
    category: str
    severity: str
    zone_id: UUID | None = None
    city_id: UUID
    upvotes: int
    downvotes: int
    verification_status: str
    ai_extracted_text: str | None = None
    media_type: str
    media_url: str | None = None
    created_at: datetime
    expires_at: datetime | None = None
