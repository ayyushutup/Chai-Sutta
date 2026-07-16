"""Train routes: city trains, line status, and delays."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.train import TrainStatus
from app.schemas.train import TrainResponse

router = APIRouter()


# ── Endpoints ───────────────────────────────────────────────────────────────


@router.get(
    "/{city_id}",
    response_model=list[TrainResponse],
    summary="Get all train statuses for a city",
)
async def get_city_trains(
    city_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get the latest recorded status for each train line in a city."""
    # Latest record per line_name via subquery
    from sqlalchemy import func, and_

    subq = (
        select(TrainStatus.line_name, func.max(TrainStatus.recorded_at).label("max_rec"))
        .where(TrainStatus.city_id == city_id)
        .group_by(TrainStatus.line_name)
        .subquery()
    )
    stmt = select(TrainStatus).join(
        subq,
        and_(
            TrainStatus.line_name == subq.c.line_name,
            TrainStatus.recorded_at == subq.c.max_rec,
        ),
    )
    result = await db.execute(stmt)
    trains = result.scalars().all()
    return [TrainResponse.model_validate(t) for t in trains]


@router.get(
    "/line/{line_name}",
    response_model=list[TrainResponse],
    summary="Get status for a specific line",
)
async def get_line_status(
    line_name: str,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get the most recent status updates for a specific train line."""
    stmt = (
        select(TrainStatus)
        .where(TrainStatus.line_name == line_name)
        .order_by(TrainStatus.recorded_at.desc())
        .limit(10)
    )
    result = await db.execute(stmt)
    trains = result.scalars().all()
    return [TrainResponse.model_validate(t) for t in trains]


@router.get(
    "/delays/{city_id}",
    response_model=list[TrainResponse],
    summary="Get delayed trains for a city",
)
async def get_delayed_trains(
    city_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get only delayed, cancelled, or diverted trains for a city."""
    stmt = (
        select(TrainStatus)
        .where(
            TrainStatus.city_id == city_id,
            TrainStatus.status != "on_time",
        )
        .order_by(TrainStatus.recorded_at.desc())
        .limit(50)
    )
    result = await db.execute(stmt)
    trains = result.scalars().all()
    return [TrainResponse.model_validate(t) for t in trains]
