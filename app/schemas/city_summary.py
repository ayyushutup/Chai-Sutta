"""City summary Pydantic schemas."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.common import MoodEnum


class CitySummaryResponse(BaseModel):
    """Schema for city summary data in API responses."""
    model_config = ConfigDict(from_attributes=True)

    summary_text: str
    mood: str
    mood_score: int
    mood_emoji: str
    trending_topics: dict | None = None
    generated_at: datetime


class CityMoodResponse(BaseModel):
    """Schema for city mood data."""
    mood: MoodEnum
    mood_score: int
    mood_emoji: str
    factors: dict
