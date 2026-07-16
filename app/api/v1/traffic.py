"""Traffic routes: city overview, zone traffic, and nearby incidents."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from geoalchemy2 import Geography
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.traffic import TrafficData
from app.models.zone import Zone
from app.schemas.traffic import TrafficResponse, TrafficZoneResponse

router = APIRouter()


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
    """Get the latest traffic data point per zone for a city."""
    # Use a sub-query to get the latest recorded_at per zone_id
    subq = (
        select(TrafficData.zone_id, func.max(TrafficData.recorded_at).label("max_rec"))
        .where(TrafficData.city_id == city_id)
        .group_by(TrafficData.zone_id)
        .subquery()
    )
    stmt = select(TrafficData).join(
        subq,
        and_(
            TrafficData.zone_id == subq.c.zone_id,
            TrafficData.recorded_at == subq.c.max_rec,
        ),
    )
    result = await db.execute(stmt)
    rows = result.scalars().all()
    return [TrafficResponse.model_validate(r) for r in rows]


@router.get(
    "/zone/{zone_id}",
    response_model=TrafficZoneResponse,
    summary="Get traffic for a zone",
)
async def get_zone_traffic(
    zone_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get latest traffic summary and data points for a specific zone."""
    # Fetch zone name
    zone_result = await db.execute(select(Zone).where(Zone.id == zone_id))
    zone = zone_result.scalar_one_or_none()
    if zone is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zone not found.")

    # Fetch latest traffic records for zone
    stmt = (
        select(TrafficData)
        .where(TrafficData.zone_id == zone_id)
        .order_by(TrafficData.recorded_at.desc())
        .limit(10)
    )
    result = await db.execute(stmt)
    rows = result.scalars().all()

    # Derive overall congestion level from latest record
    overall = rows[0].congestion_level if rows else "unknown"

    return TrafficZoneResponse(
        zone_name=zone.name,
        overall_congestion=overall,
        data_points=[TrafficResponse.model_validate(r) for r in rows],
    )


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
    """Get traffic data points near a geographic coordinate."""
    radius_meters = radius_km * 1000.0
    point = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)

    stmt = select(TrafficData).where(
        func.ST_DWithin(
            func.cast(TrafficData.location, Geography),
            func.cast(point, Geography),
            radius_meters,
        )
    ).order_by(
        func.ST_Distance(
            func.cast(TrafficData.location, Geography),
            func.cast(point, Geography),
        )
    ).limit(50)

    result = await db.execute(stmt)
    rows = result.scalars().all()
    return [TrafficResponse.model_validate(r) for r in rows]
