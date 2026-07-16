"""Search routes: cross-content full-text search and autocomplete."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, literal, select, union_all
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.event import Event
from app.models.news import NewsArticle
from app.models.report import CommunityReport
from app.schemas.search import SearchResponse, SearchResultItem

router = APIRouter()


# ── Endpoints ───────────────────────────────────────────────────────────────


@router.get(
    "/",
    response_model=SearchResponse,
    summary="Search across all content",
)
async def search(
    q: str = Query(..., min_length=1, max_length=200, description="Search query"),
    content_type: str | None = Query(default=None, description="Filter by content type: news, event, report"),
    city_id: UUID | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Search across news, events, and community reports using PostgreSQL full-text search.

    Uses each model's ``search_vector`` tsvector column (GIN indexed) where available,
    falling back to ``ILIKE`` for models that may not have vectors populated yet.
    """
    pattern = f"%{q}%"
    ts_query = func.plainto_tsquery("english", q)

    results: list[SearchResultItem] = []

    # ── News ─────────────────────────────────────────────────────────────────
    if content_type in (None, "news"):
        news_stmt = (
            select(
                NewsArticle.id,
                NewsArticle.title,
                NewsArticle.summary,
                NewsArticle.category,
                NewsArticle.created_at,
                func.coalesce(
                    func.ts_rank(NewsArticle.search_vector, ts_query),
                    literal(0.1),
                ).label("score"),
            )
            .where(
                NewsArticle.status == "published",
                (
                    NewsArticle.search_vector.op("@@")(ts_query)
                    | NewsArticle.title.ilike(pattern)
                ),
            )
        )
        if city_id:
            news_stmt = news_stmt.where(NewsArticle.city_id == city_id)
        news_result = await db.execute(news_stmt.order_by(func.ts_rank(NewsArticle.search_vector, ts_query).desc()).limit(page_size))
        for row in news_result.all():
            results.append(
                SearchResultItem(
                    id=row.id,
                    type="news",
                    title=row.title,
                    snippet=row.summary or row.title,
                    category=row.category,
                    relevance_score=float(row.score) if row.score else 0.1,
                    created_at=row.created_at,
                )
            )

    # ── Events ───────────────────────────────────────────────────────────────
    if content_type in (None, "event"):
        event_stmt = (
            select(
                Event.id,
                Event.title,
                Event.description,
                Event.category,
                Event.created_at,
                func.coalesce(
                    func.ts_rank(Event.search_vector, ts_query),
                    literal(0.1),
                ).label("score"),
            )
            .where(
                Event.is_active == True,
                (
                    Event.search_vector.op("@@")(ts_query)
                    | Event.title.ilike(pattern)
                ),
            )
        )
        if city_id:
            event_stmt = event_stmt.where(Event.city_id == city_id)
        event_result = await db.execute(event_stmt.order_by(func.ts_rank(Event.search_vector, ts_query).desc()).limit(page_size))
        for row in event_result.all():
            results.append(
                SearchResultItem(
                    id=row.id,
                    type="event",
                    title=row.title,
                    snippet=row.description or row.title,
                    category=row.category,
                    relevance_score=float(row.score) if row.score else 0.1,
                    created_at=row.created_at,
                )
            )

    # ── Community Reports ─────────────────────────────────────────────────────
    if content_type in (None, "report"):
        report_stmt = (
            select(
                CommunityReport.id,
                CommunityReport.content,
                CommunityReport.category,
                CommunityReport.created_at,
                literal(0.1).label("score"),
            )
            .where(
                CommunityReport.is_active == True,
                CommunityReport.content.ilike(pattern),
            )
        )
        if city_id:
            report_stmt = report_stmt.where(CommunityReport.city_id == city_id)
        report_result = await db.execute(report_stmt.limit(page_size))
        for row in report_result.all():
            results.append(
                SearchResultItem(
                    id=row.id,
                    type="report",
                    title=row.content[:80] + ("…" if len(row.content) > 80 else ""),
                    snippet=row.content,
                    category=row.category,
                    relevance_score=float(row.score),
                    created_at=row.created_at,
                )
            )

    # Sort all results by relevance descending, then paginate in-memory
    results.sort(key=lambda r: r.relevance_score, reverse=True)
    total = len(results)
    paginated = results[(page - 1) * page_size: page * page_size]

    return SearchResponse(results=paginated, total=total, query=q)


@router.get(
    "/suggest",
    response_model=list[str],
    summary="Get autocomplete suggestions",
)
async def suggest(
    q: str = Query(..., min_length=1, max_length=100, description="Partial query"),
    city_id: UUID | None = Query(default=None),
    limit: int = Query(default=5, ge=1, le=10),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get autocomplete suggestions from news titles and event titles."""
    pattern = f"{q}%"
    suggestions: list[str] = []

    # News titles
    news_stmt = (
        select(NewsArticle.title)
        .where(NewsArticle.title.ilike(pattern), NewsArticle.status == "published")
        .distinct()
        .limit(limit)
    )
    if city_id:
        news_stmt = news_stmt.where(NewsArticle.city_id == city_id)
    news_result = await db.execute(news_stmt)
    suggestions.extend(row.title for row in news_result.all())

    # Event titles
    remaining = limit - len(suggestions)
    if remaining > 0:
        event_stmt = (
            select(Event.title)
            .where(Event.title.ilike(pattern), Event.is_active == True)
            .distinct()
            .limit(remaining)
        )
        if city_id:
            event_stmt = event_stmt.where(Event.city_id == city_id)
        event_result = await db.execute(event_stmt)
        suggestions.extend(row.title for row in event_result.all())

    return suggestions[:limit]
