"""Train routes: city trains, line status, and delays."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db

router = APIRouter()


# ── Schemas ─────────────────────────────────────────────────────────────────


class TrainResponse(BaseModel):
    """Train line or service status."""
    id: UUID
    city_id: UUID
    line_name: str
    status: str  # on_time, delayed, cancelled, suspended
    delay_minutes: int | None = None
    reason: str | None = None
    origin: str | None = None
    destination: str | None = None
    scheduled_time: str | None = None
    expected_time: str | None = None
    platform: str | None = None
    updated_at: str | None = None

    model_config = {"from_attributes": True}


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
    """Get all train line statuses for a city."""
    # TODO: Implement train status service
    return []


@router.get(
    "/line/{line_name}",
    response_model=list[TrainResponse],
    summary="Get status for a specific line",
)
async def get_line_status(
    line_name: str,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get status updates for a specific train line."""
    # TODO: Implement line status service
    return []


@router.get(
    "/delays/{city_id}",
    response_model=list[TrainResponse],
    summary="Get delayed trains for a city",
)
async def get_delayed_trains(
    city_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get only delayed or disrupted trains for a city."""
    # TODO: Implement delayed trains filter
    return []
