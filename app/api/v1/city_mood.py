"""City mood routes: sentiment analysis of a city derived from CitySummary records."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.city_summary import CitySummary
from app.schemas.city_summary import CityMoodResponse
from app.schemas.common import PaginatedResponse

router = APIRouter()


# ── Schemas ─────────────────────────────────────────────────────────────────

# CityMoodResponse is imported from app/schemas/city_summary.py:
#   mood: MoodEnum, mood_score: int, mood_emoji: str, factors: dict


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
    """Get the current aggregate mood / sentiment for a city.

    Reads from the latest ``CitySummary`` record which stores
    mood, mood_score, mood_emoji, and a data_snapshot.
    """
    result = await db.execute(
        select(CitySummary)
        .where(CitySummary.city_id == city_id)
        .order_by(CitySummary.generated_at.desc())
        .limit(1)
    )
    summary = result.scalar_one_or_none()
    if summary is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No mood data found for this city.",
        )

    return CityMoodResponse(
        mood=summary.mood,
        mood_score=summary.mood_score,
        mood_emoji=summary.mood_emoji,
        factors=summary.data_snapshot or {},
    )


@router.get(
    "/history/{city_id}",
    response_model=PaginatedResponse[CityMoodResponse],
    summary="Get city mood history",
)
async def get_mood_history(
    city_id: UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get historical mood data for a city, newest first."""
    base_stmt = select(CitySummary).where(CitySummary.city_id == city_id)

    total = (
        await db.execute(select(func.count()).select_from(base_stmt.subquery()))
    ).scalar_one()

    stmt = (
        base_stmt
        .order_by(CitySummary.generated_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    summaries = result.scalars().all()

    items = [
        CityMoodResponse(
            mood=s.mood,
            mood_score=s.mood_score,
            mood_emoji=s.mood_emoji,
            factors=s.data_snapshot or {},
        )
        for s in summaries
    ]

    return PaginatedResponse(items=items, total=total, page=page, page_size=page_size)
