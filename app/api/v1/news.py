"""News routes: list, detail, and city feed."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CommonQueryParams, get_db

router = APIRouter()


# ── Schemas ─────────────────────────────────────────────────────────────────


class NewsResponse(BaseModel):
    """News article response."""
    id: UUID
    title: str
    summary: str
    content: str | None = None
    source: str
    source_url: str | None = None
    category: str | None = None
    city_id: UUID | None = None
    zone_id: UUID | None = None
    image_url: str | None = None
    published_at: str | None = None
    sentiment_score: float | None = None

    model_config = {"from_attributes": True}


class PaginatedNewsResponse(BaseModel):
    """Paginated news list response."""
    items: list[NewsResponse]
    total: int
    page: int
    page_size: int
    has_next: bool


# ── Endpoints ───────────────────────────────────────────────────────────────


@router.get(
    "/",
    response_model=PaginatedNewsResponse,
    summary="List news articles",
)
async def list_news(
    city_id: UUID | None = Query(default=None),
    zone_id: UUID | None = Query(default=None),
    category: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """List news articles with optional city, zone, and category filters."""
    # TODO: Implement news listing service
    return PaginatedNewsResponse(items=[], total=0, page=page, page_size=page_size, has_next=False)


@router.get(
    "/{news_id}",
    response_model=NewsResponse,
    summary="Get a single news article",
)
async def get_news(
    news_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get a single news article by ID."""
    # TODO: Implement news detail service
    raise NotImplementedError("News detail not yet implemented.")


@router.get(
    "/feed/{city_id}",
    response_model=list[NewsResponse],
    summary="Get news feed for a city",
)
async def get_city_feed(
    city_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get the curated news feed for a specific city."""
    # TODO: Implement city feed service
    return []
