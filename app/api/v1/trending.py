"""Trending routes: trending topics and top discussions."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.social_mention import SocialMention

router = APIRouter()


# ── Schemas ─────────────────────────────────────────────────────────────────


class TrendingTopic(BaseModel):
    """A trending topic aggregated from social mentions."""
    keyword: str
    mention_count: int
    platform: str | None = None
    category: str | None = None


class TrendingDiscussion(BaseModel):
    """A top social media discussion."""
    post_id: str | None = None
    content: str
    author: str | None = None
    platform: str
    engagement_score: int
    category: str | None = None


# ── Endpoints ───────────────────────────────────────────────────────────────


@router.get(
    "/{city_id}",
    response_model=list[TrendingTopic],
    summary="Get trending topics for a city",
)
async def get_trending(
    city_id: UUID,
    limit: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get trending topics for a city by aggregating social mentions.

    Groups mentions by category and platform, returning the top keywords
    sorted by mention count.
    """
    # Aggregate by category (used as a proxy keyword bucket) and platform
    stmt = (
        select(
            SocialMention.category,
            SocialMention.platform,
            func.count(SocialMention.id).label("mention_count"),
        )
        .where(SocialMention.city_id == city_id, SocialMention.category.isnot(None))
        .group_by(SocialMention.category, SocialMention.platform)
        .order_by(func.count(SocialMention.id).desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    rows = result.all()

    return [
        TrendingTopic(
            keyword=row.category,
            mention_count=row.mention_count,
            platform=row.platform,
            category=row.category,
        )
        for row in rows
    ]


@router.get(
    "/discussions/{city_id}",
    response_model=list[TrendingDiscussion],
    summary="Get top discussions for a city",
)
async def get_discussions(
    city_id: UUID,
    limit: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get top social media discussions for a city, sorted by engagement score."""
    stmt = (
        select(SocialMention)
        .where(SocialMention.city_id == city_id)
        .order_by(SocialMention.engagement_score.desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    mentions = result.scalars().all()

    return [
        TrendingDiscussion(
            post_id=m.post_id,
            content=m.content,
            author=m.author,
            platform=m.platform,
            engagement_score=m.engagement_score,
            category=m.category,
        )
        for m in mentions
    ]
