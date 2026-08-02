"""Ingestion background tasks: news feeds, weather, and traffic data ingestion."""
from __future__ import annotations

from datetime import datetime, timezone
import logging
from uuid import UUID

import httpx
from geoalchemy2.shape import to_shape
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.models.city import City
from app.models.weather import WeatherData
from app.models.zone import Zone

logger = logging.getLogger("chai_sutta.workers.ingestion")

# WMO Weather interpretation codes (WW) to condition text
WMO_CODE_MAP = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def _create_db_session_factory() -> async_sessionmaker[AsyncSession]:
    """Helper to create DB session factory for worker tasks if not provided in ctx."""
    engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)
    return async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def ingest_news_feeds(ctx: dict, city_id: str | None = None) -> str:
    """Ingest news articles from RSS feeds and web scrapers.

    Args:
        ctx: ARQ worker context dict (contains DB session, Redis, etc.).
        city_id: Optional UUID string to limit ingestion to a specific city.

    Returns:
        Summary string of ingestion results.
    """
    logger.info("ingest_news_feeds called | city_id=%s", city_id)
    # Placeholder — real implementation goes here
    return "ingest_news_feeds: not yet implemented"


async def ingest_weather(ctx: dict, city_id: str | None = None) -> str:
    """Fetch and persist weather snapshots for all active cities and zones via Open-Meteo API.

    Args:
        ctx: ARQ worker context.
        city_id: Optional UUID string to limit to a specific city.
    """
    logger.info("ingest_weather starting | city_id=%s", city_id)

    session_factory = ctx.get("db_session_factory")
    if not session_factory:
        session_factory = _create_db_session_factory()

    records_created = 0

    async with session_factory() as db:
        # Query active cities and prefetch their zones
        stmt = select(City).where(City.is_active == True)
        if city_id:
            stmt = stmt.where(City.id == UUID(city_id))
        
        result = await db.execute(stmt)
        cities = result.scalars().all()

        if not cities:
            logger.info("No active cities found for weather ingestion.")
            return "ingest_weather: 0 records created (no active cities)"

        async with httpx.AsyncClient(timeout=15.0) as http_client:
            for city in cities:
                zones = city.zones
                if not zones:
                    logger.warning("City %s (%s) has no zones; skipping weather ingestion.", city.name, city.id)
                    continue

                for zone in zones:
                    if not zone.is_active or zone.centroid is None:
                        continue

                    # Extract lat/lon from zone centroid Point geometry
                    shape = to_shape(zone.centroid)
                    lat, lon = shape.y, shape.x

                    # Call Open-Meteo Forecast API
                    url = (
                        f"https://api.open-meteo.com/v1/forecast?"
                        f"latitude={lat}&longitude={lon}&"
                        f"current=temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation,weather_code&"
                        f"hourly=temperature_2m,relative_humidity_2m,precipitation,weather_code&"
                        f"daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code&"
                        f"timezone=auto"
                    )

                    try:
                        resp = await http_client.get(url)
                        resp.raise_for_status()
                        data = resp.json()
                    except Exception as err:
                        logger.error("Failed to fetch weather for zone %s (%s): %s", zone.name, zone.id, err)
                        continue

                    current = data.get("current", {})
                    weather_code = current.get("weather_code", 0)
                    condition_text = WMO_CODE_MAP.get(weather_code, "Unknown")

                    # Severity heuristic
                    severity = "normal"
                    if weather_code in (82, 95, 96, 99):
                        severity = "warning"

                    weather_record = WeatherData(
                        zone_id=zone.id,
                        city_id=city.id,
                        temperature=current.get("temperature_2m", 0.0),
                        humidity=float(current.get("relative_humidity_2m", 0)),
                        wind_speed=current.get("wind_speed_10m", 0.0),
                        rain=current.get("precipitation", 0.0),
                        condition=condition_text,
                        weather_code=weather_code,
                        severity=severity,
                        hourly_forecast=data.get("hourly"),
                        daily_forecast=data.get("daily"),
                        recorded_at=datetime.now(timezone.utc),
                    )

                    db.add(weather_record)
                    records_created += 1

        await db.commit()

    logger.info("ingest_weather completed | records_created=%d", records_created)
    return f"ingest_weather: successfully created {records_created} weather records"


async def ingest_traffic(ctx: dict, city_id: str | None = None) -> str:
    """Fetch and persist traffic snapshots from TomTom API.

    Args:
        ctx: ARQ worker context.
        city_id: Optional UUID string to limit to a specific city.
    """
    logger.info("ingest_traffic called | city_id=%s", city_id)
    # Placeholder — real implementation goes here
    return "ingest_traffic: not yet implemented"


async def ingest_social_mentions(ctx: dict, city_id: str | None = None) -> str:
    """Scrape social media mentions from Twitter/Reddit for city topics.

    Args:
        ctx: ARQ worker context.
        city_id: Optional city UUID string.
    """
    logger.info("ingest_social_mentions called | city_id=%s", city_id)
    # Placeholder — real implementation goes here
    return "ingest_social_mentions: not yet implemented"
