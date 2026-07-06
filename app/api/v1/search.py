"""Search routes: cross-content search and autocomplete."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db

router = APIRouter()


# ── Schemas ─────────────────────────────────────────────────────────────────


class SearchResultItem(BaseModel):
    """A single search result."""
    id: UUID
    content_type: str  # news, event, report, place
    title: str
    snippet: str | None = None
    score: float | None = None
    url: str | None = None
    metadata: dict | None = None


class SearchResponse(BaseModel):
    """Search results response."""
    query: str
    total: int
    items: list[SearchResultItem]
    page: int
    page_size: int
    has_next: bool


# ── Endpoints ───────────────────────────────────────────────────────────────


@router.get(
    "/",
    response_model=SearchResponse,
    summary="Search across all content",
)
async def search(
    q: str = Query(..., min_length=1, max_length=200, description="Search query"),
    content_type: str | None = Query(default=None, description="Filter by content type"),
    city_id: UUID | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Search across all content types: news, events, reports, places.

    Uses both full-text and vector similarity search.
    """
    # TODO: Implement search service with Qdrant + PostgreSQL
    return SearchResponse(
        query=q,
        total=0,
        items=[],
        page=page,
        page_size=page_size,
        has_next=False,
    )


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
    """Get autocomplete suggestions based on a partial query."""
    # TODO: Implement suggestion service
    return []
