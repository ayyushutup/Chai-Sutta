"""WeatherData model – periodic weather snapshots per zone."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.city import City
    from app.models.zone import Zone


class WeatherData(TimestampMixin, Base):
    """A weather data snapshot for a specific zone.

    Attributes:
        zone_id: Zone FK.
        city_id: City FK.
        temperature: Temperature in °C.
        humidity: Relative humidity (%).
        wind_speed: Wind speed (km/h).
        rain: Rainfall (mm), defaults to 0.
        condition: Human-readable weather condition.
        weather_code: Numeric weather code (provider-specific).
        severity: Alert severity (normal / advisory / warning / severe).
        hourly_forecast: JSONB hourly forecast data.
        daily_forecast: JSONB daily forecast data.
        alerts: JSONB weather alerts.
        recorded_at: When this data was recorded.
    """

    __tablename__ = "weather_data"

    zone_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("zones.id"), nullable=False,
    )
    city_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cities.id"), nullable=False,
    )
    temperature: Mapped[float] = mapped_column(
        Float, nullable=False,
    )
    humidity: Mapped[float] = mapped_column(
        Float, nullable=False,
    )
    wind_speed: Mapped[float] = mapped_column(
        Float, nullable=False,
    )
    rain: Mapped[float] = mapped_column(
        Float, default=0, server_default=text("0"),
    )
    condition: Mapped[str] = mapped_column(
        String(100), nullable=False,
    )
    weather_code: Mapped[int | None] = mapped_column(
        Integer, nullable=True,
    )
    severity: Mapped[str] = mapped_column(
        String(20), default="normal", server_default=text("'normal'"), nullable=False,
    )
    hourly_forecast: Mapped[dict | None] = mapped_column(
        JSONB, nullable=True,
    )
    daily_forecast: Mapped[dict | None] = mapped_column(
        JSONB, nullable=True,
    )
    alerts: Mapped[dict | None] = mapped_column(
        JSONB, nullable=True,
    )
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
    )

    # -- relationships --
    zone: Mapped[Zone] = relationship()
    city: Mapped[City] = relationship()

    def __repr__(self) -> str:
        return f"<WeatherData zone_id={self.zone_id} temp={self.temperature}>"
