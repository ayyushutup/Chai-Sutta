"""Traffic routes: city overview, zone traffic, and nearby incidents."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import GeoQueryParams, get_db

router = APIRouter()


# ── Schemas ─────────────────────────────────────────────────────────────────


class TrafficResponse(BaseModel):
    """Traffic incident or flow data."""
    id: UUID
    city_id: UUID
    type: str  # incident, congestion, closure
    severity: str  # low, medium, high, critical
    title: str
    description: str | None = None
    lat: float | None = None
    lon: float | None = None
    road_name: str | None = None
    delay_minutes: int | None = None
    updated_at: str | None = None

    model_config = {"from_attributes": True}


class TrafficZoneResponse(BaseModel):
    """Traffic summary for a zone."""
    zone_id: UUID
    congestion_level: str  # free, light, moderate, heavy, gridlock
    average_speed_kph: float | None = None
    incidents: list[TrafficResponse]
    updated_at: str | None = None


# ── Endpoints ───────────────────────────────────────────────────────────────


@router.get(
    "/{city_id}",
    response_model=list[TrafficResponse],
    summary="Get traffic overview for a city",
)
async def get_city_traffic(
    city_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get all traffic incidents and flow data for a city."""
    # TODO: Implement traffic service
    return []


@router.get(
    "/zone/{zone_id}",
    response_model=TrafficZoneResponse,
    summary="Get traffic for a zone",
)
async def get_zone_traffic(
    zone_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get traffic summary and incidents for a specific zone."""
    # TODO: Implement zone traffic service
    raise NotImplementedError("Zone traffic not yet implemented.")


@router.get(
    "/nearby",
    response_model=list[TrafficResponse],
    summary="Get traffic near a point",
)
async def get_nearby_traffic(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(default=5.0, gt=0, le=50),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get traffic incidents near a geographic point."""
    # TODO: Implement nearby traffic service
    return []
