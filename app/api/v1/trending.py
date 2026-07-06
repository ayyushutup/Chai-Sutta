"""Trending routes: trending topics and top discussions."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db

router = APIRouter()


# ── Schemas ─────────────────────────────────────────────────────────────────


class TrendingTopic(BaseModel):
    """A trending topic in a city."""
    keyword: str
    mention_count: int
    sentiment: str | None = None  # positive, negative, neutral
    category: str | None = None
    source: str | None = None  # reddit, twitter, news


class TrendingDiscussion(BaseModel):
    """A top discussion from social media."""
    title: str
    url: str | None = None
    source: str
    score: int | None = None
    comment_count: int | None = None
    created_at: str | None = None


# ── Endpoints ───────────────────────────────────────────────────────────────


@router.get(
    "/{city_id}",
    response_model=list[TrendingTopic],
    summary="Get trending topics for a city",
)
async def get_trending(
    city_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get the current trending topics for a city, aggregated from multiple sources."""
    # TODO: Implement trending service
    return []


@router.get(
    "/discussions/{city_id}",
    response_model=list[TrendingDiscussion],
    summary="Get top discussions for a city",
)
async def get_discussions(
    city_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get top social media discussions for a city."""
    # TODO: Implement discussions service
    return []
