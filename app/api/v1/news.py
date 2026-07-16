"""News routes: list, detail, and city feed."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.news import NewsArticle
from app.schemas.common import PaginatedResponse
from app.schemas.news import NewsResponse

router = APIRouter()


# ── Endpoints ───────────────────────────────────────────────────────────────


@router.get(
    "/",
    response_model=PaginatedResponse[NewsResponse],
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
    stmt = select(NewsArticle).where(NewsArticle.status == "published")

    if city_id:
        stmt = stmt.where(NewsArticle.city_id == city_id)
    if zone_id:
        stmt = stmt.where(NewsArticle.zone_id == zone_id)
    if category:
        stmt = stmt.where(NewsArticle.category == category)

    stmt = stmt.order_by(NewsArticle.published_at.desc())

    # Total count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar_one()

    # Paginate
    stmt = stmt.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(stmt)
    articles = result.scalars().all()

    return PaginatedResponse(
        items=[NewsResponse.model_validate(a) for a in articles],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/feed/{city_id}",
    response_model=list[NewsResponse],
    summary="Get news feed for a city",
)
async def get_city_feed(
    city_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get the curated news feed for a specific city, ordered by importance then recency."""
    stmt = (
        select(NewsArticle)
        .where(NewsArticle.city_id == city_id, NewsArticle.status == "published")
        .order_by(NewsArticle.importance_score.desc(), NewsArticle.published_at.desc())
        .limit(20)
    )
    result = await db.execute(stmt)
    articles = result.scalars().all()
    return [NewsResponse.model_validate(a) for a in articles]


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
    result = await db.execute(
        select(NewsArticle).where(NewsArticle.id == news_id)
    )
    article = result.scalar_one_or_none()
    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News article not found.")
    return NewsResponse.model_validate(article)
