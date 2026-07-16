"""Weather routes: current conditions, zone weather, and forecasts."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.weather import WeatherData
from app.schemas.weather import WeatherResponse

router = APIRouter()


# ── Endpoints ───────────────────────────────────────────────────────────────


@router.get(
    "/{city_id}",
    response_model=WeatherResponse,
    summary="Get current weather for a city",
)
async def get_city_weather(
    city_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get the most recent weather snapshot for a city."""
    result = await db.execute(
        select(WeatherData)
        .where(WeatherData.city_id == city_id)
        .order_by(WeatherData.recorded_at.desc())
        .limit(1)
    )
    weather = result.scalar_one_or_none()
    if weather is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No weather data found for this city.",
        )
    return WeatherResponse.model_validate(weather)


@router.get(
    "/zone/{zone_id}",
    response_model=WeatherResponse,
    summary="Get weather for a zone",
)
async def get_zone_weather(
    zone_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get the most recent weather snapshot for a specific zone."""
    result = await db.execute(
        select(WeatherData)
        .where(WeatherData.zone_id == zone_id)
        .order_by(WeatherData.recorded_at.desc())
        .limit(1)
    )
    weather = result.scalar_one_or_none()
    if weather is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No weather data found for this zone.",
        )
    return WeatherResponse.model_validate(weather)


@router.get(
    "/forecast/{city_id}",
    response_model=WeatherResponse,
    summary="Get weather forecast for a city",
)
async def get_forecast(
    city_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get the latest weather record including forecast data for a city.

    The returned record includes ``hourly_forecast`` and ``daily_forecast``
    JSONB fields populated by the ingestion worker.
    """
    result = await db.execute(
        select(WeatherData)
        .where(WeatherData.city_id == city_id)
        .order_by(WeatherData.recorded_at.desc())
        .limit(1)
    )
    weather = result.scalar_one_or_none()
    if weather is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No forecast data found for this city.",
        )
    return WeatherResponse.model_validate(weather)
