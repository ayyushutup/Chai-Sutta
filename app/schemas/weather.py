"""Weather-related Pydantic schemas."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WeatherResponse(BaseModel):
    """Schema for weather data in API responses."""
    model_config = ConfigDict(from_attributes=True)

    temperature: float
    humidity: float
    wind_speed: float
    rain: float
    condition: str
    severity: str
    weather_code: int | None = None
    hourly_forecast: dict | None = None
    daily_forecast: dict | None = None
    alerts: dict | None = None
    recorded_at: datetime
