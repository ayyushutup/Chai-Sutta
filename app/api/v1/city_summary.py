"""City summary routes: AI-generated city intelligence summaries."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.city_summary import CitySummary
from app.schemas.city_summary import CitySummaryResponse
from app.schemas.common import PaginatedResponse

router = APIRouter()


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
            detail="No city summary found for this city.",
        )
    return CitySummaryResponse.model_validate(summary)


@router.get(
    "/history/{city_id}",
    response_model=PaginatedResponse[CitySummaryResponse],
    summary="Get historical city summaries",
)
async def get_summary_history(
    city_id: UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get past city summaries with pagination, newest first."""
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

    return PaginatedResponse(
        items=[CitySummaryResponse.model_validate(s) for s in summaries],
        total=total,
        page=page,
        page_size=page_size,
    )
