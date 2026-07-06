"""City summary routes: AI-generated city intelligence summaries."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db

router = APIRouter()


# ── Schemas ─────────────────────────────────────────────────────────────────


class CitySummaryResponse(BaseModel):
    """AI-generated city summary."""
    id: UUID
    city_id: UUID
    summary_text: str
    key_highlights: list[str] | None = None
    weather_snippet: str | None = None
    traffic_snippet: str | None = None
    news_snippet: str | None = None
    events_snippet: str | None = None
    generated_at: str | None = None
    model_used: str | None = None

    model_config = {"from_attributes": True}


# ── Endpoints ───────────────────────────────────────────────────────────────


@router.get(
    "/{city_id}",
    response_model=CitySummaryResponse,
    summary="Get latest city summary",
)
async def get_city_summary(
    city_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get the most recent AI-generated summary for a city."""
    # TODO: Implement city summary service
    raise NotImplementedError("City summary not yet implemented.")


@router.get(
    "/history/{city_id}",
    response_model=list[CitySummaryResponse],
    summary="Get historical city summaries",
)
async def get_summary_history(
    city_id: UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get past city summaries with pagination."""
    # TODO: Implement summary history service
    return []
