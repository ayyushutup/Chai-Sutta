"""City mood routes: sentiment analysis of a city."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db

router = APIRouter()


# ── Schemas ─────────────────────────────────────────────────────────────────


class MoodBreakdown(BaseModel):
    """Sentiment breakdown by source."""
    source: str  # twitter, reddit, news, reports
    positive: float
    neutral: float
    negative: float
    sample_size: int


class CityMoodResponse(BaseModel):
    """City mood / sentiment response."""
    id: UUID
    city_id: UUID
    overall_mood: str  # happy, neutral, concerned, angry, excited
    mood_score: float  # -1.0 to 1.0
    mood_emoji: str | None = None
    breakdown: list[MoodBreakdown] | None = None
    top_positive_topic: str | None = None
    top_negative_topic: str | None = None
    measured_at: str | None = None

    model_config = {"from_attributes": True}


# ── Endpoints ───────────────────────────────────────────────────────────────


@router.get(
    "/{city_id}",
    response_model=CityMoodResponse,
    summary="Get current city mood",
)
async def get_city_mood(
    city_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get the current aggregate mood / sentiment for a city."""
    # TODO: Implement city mood service
    raise NotImplementedError("City mood not yet implemented.")


@router.get(
    "/history/{city_id}",
    response_model=list[CityMoodResponse],
    summary="Get city mood history",
)
async def get_mood_history(
    city_id: UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get historical mood data for a city."""
    # TODO: Implement mood history service
    return []
