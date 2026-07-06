"""Weather routes: current conditions, zone weather, and forecasts."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db

router = APIRouter()


# ── Schemas ─────────────────────────────────────────────────────────────────


class ForecastEntry(BaseModel):
    """Single forecast entry."""
    datetime: str
    temp_c: float
    condition: str
    humidity: int | None = None
    wind_kph: float | None = None
    icon_url: str | None = None


class WeatherResponse(BaseModel):
    """Weather data response."""
    city_id: UUID
    zone_id: UUID | None = None
    temp_c: float
    feels_like_c: float | None = None
    condition: str
    humidity: int | None = None
    wind_kph: float | None = None
    aqi: int | None = None
    aqi_label: str | None = None
    icon_url: str | None = None
    updated_at: str | None = None
    forecast: list[ForecastEntry] | None = None

    model_config = {"from_attributes": True}


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
    """Get the current weather conditions for a city."""
    # TODO: Implement weather service
    raise NotImplementedError("City weather not yet implemented.")


@router.get(
    "/zone/{zone_id}",
    response_model=WeatherResponse,
    summary="Get weather for a zone",
)
async def get_zone_weather(
    zone_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get the current weather conditions for a specific zone."""
    # TODO: Implement zone weather service
    raise NotImplementedError("Zone weather not yet implemented.")


@router.get(
    "/forecast/{city_id}",
    response_model=WeatherResponse,
    summary="Get weather forecast for a city",
)
async def get_forecast(
    city_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get multi-day weather forecast for a city."""
    # TODO: Implement forecast service
    raise NotImplementedError("Weather forecast not yet implemented.")
