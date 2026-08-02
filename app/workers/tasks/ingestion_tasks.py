"""Ingestion background tasks: news feeds, weather, and traffic data ingestion."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import logging
from time import mktime
from uuid import UUID

import feedparser
import httpx
from geoalchemy2.shape import to_shape
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.core.geo import point_from_coords
from app.models.city import City
from app.models.news import NewsArticle
from app.models.traffic import TrafficData
from app.models.weather import WeatherData
from app.models.zone import Zone

logger = logging.getLogger("chai_sutta.workers.ingestion")

# Default RSS feed sources per city category/general
DEFAULT_RSS_FEEDS = [
    {"source_name": "NDTV News", "category": "general", "url": "https://feeds.feedburner.com/ndtvnews-top-stories"},
    {"source_name": "Times of India", "category": "general", "url": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"},
    {"source_name": "The Hindu", "category": "general", "url": "https://www.thehindu.com/news/national/feeder/default.rss"},
    {"source_name": "Indian Express", "category": "general", "url": "https://indianexpress.com/section/india/feed/"},
]

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


def _compute_content_hash(source_url: str, title: str) -> str:
    """Generate SHA-256 hash for article deduplication."""
    data = f"{source_url.strip().lower()}:{title.strip().lower()}"
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


async def ingest_news_feeds(ctx: dict, city_id: str | None = None) -> str:
    """Ingest news articles from RSS feeds, deduplicate using content_hash, and associate with active cities.

    Args:
        ctx: ARQ worker context dict (contains DB session, Redis, etc.).
        city_id: Optional UUID string to limit ingestion to a specific city.

    Returns:
        Summary string of ingestion results.
    """
    logger.info("ingest_news_feeds starting | city_id=%s", city_id)

    session_factory = ctx.get("db_session_factory")
    if not session_factory:
        session_factory = _create_db_session_factory()

    articles_created = 0
    duplicates_skipped = 0

    async with session_factory() as db:
        # Fetch active cities
        stmt = select(City).where(City.is_active == True)
        if city_id:
            stmt = stmt.where(City.id == UUID(city_id))
        
        result = await db.execute(stmt)
        cities = result.scalars().all()

        if not cities:
            logger.info("No active cities found for news feed ingestion.")
            return "ingest_news_feeds: 0 articles created (no active cities)"

        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as http_client:
            for feed in DEFAULT_RSS_FEEDS:
                feed_url = feed["url"]
                source_name = feed["source_name"]
                default_category = feed["category"]

                try:
                    resp = await http_client.get(feed_url)
                    resp.raise_for_status()
                    parsed = feedparser.parse(resp.text)
                except Exception as err:
                    logger.error("Failed to fetch RSS feed %s (%s): %s", source_name, feed_url, err)
                    continue

                for entry in parsed.entries:
                    title = getattr(entry, "title", "").strip()
                    source_url = getattr(entry, "link", "").strip()

                    if not title or not source_url:
                        continue

                    # Deduplication check via SHA-256 hash
                    content_hash = _compute_content_hash(source_url, title)
                    existing_check = await db.execute(
                        select(NewsArticle.id).where(NewsArticle.content_hash == content_hash)
                    )
                    if existing_check.scalar_one_or_none() is not None:
                        duplicates_skipped += 1
                        continue

                    # Article summary / content parsing
                    summary = getattr(entry, "summary", "") or getattr(entry, "description", None)
                    content = getattr(entry, "content", [{}])[0].get("value", None) if hasattr(entry, "content") else None

                    # Published timestamp
                    published_at = datetime.now(timezone.utc)
                    if hasattr(entry, "published_parsed") and entry.published_parsed:
                        published_at = datetime.fromtimestamp(mktime(entry.published_parsed), tz=timezone.utc)

                    # Simple city matching logic based on headline/summary
                    # Assign to all matching cities or default to the first city if general
                    full_text = f"{title} {summary or ''}".lower()
                    matched_cities = [c for c in cities if c.name.lower() in full_text]
                    target_cities = matched_cities if matched_cities else [cities[0]]

                    for target_city in target_cities:
                        article = NewsArticle(
                            title=title,
                            content=content,
                            summary=summary,
                            source_url=source_url,
                            source_name=source_name,
                            category=default_category,
                            importance_score=50,  # default baseline importance
                            city_id=target_city.id,
                            content_hash=f"{content_hash}_{target_city.id}",  # unique per city mapping
                            status="published",
                            published_at=published_at,
                        )
                        db.add(article)
                        articles_created += 1

        await db.commit()

    logger.info("ingest_news_feeds completed | created=%d skipped_duplicates=%d", articles_created, duplicates_skipped)
    return f"ingest_news_feeds: successfully created {articles_created} articles ({duplicates_skipped} duplicates skipped)"


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
    """Fetch and persist traffic snapshots from TomTom API or generate spatial baseline metrics.

    Args:
        ctx: ARQ worker context.
        city_id: Optional UUID string to limit to a specific city.
    """
    logger.info("ingest_traffic starting | city_id=%s", city_id)

    session_factory = ctx.get("db_session_factory")
    if not session_factory:
        session_factory = _create_db_session_factory()

    records_created = 0

    async with session_factory() as db:
        stmt = select(City).where(City.is_active == True)
        if city_id:
            stmt = stmt.where(City.id == UUID(city_id))

        result = await db.execute(stmt)
        cities = result.scalars().all()

        if not cities:
            logger.info("No active cities found for traffic ingestion.")
            return "ingest_traffic: 0 records created (no active cities)"

        async with httpx.AsyncClient(timeout=15.0) as http_client:
            for city in cities:
                zones = city.zones
                for zone in zones:
                    if not zone.is_active or zone.centroid is None:
                        continue

                    shape = to_shape(zone.centroid)
                    lat, lon = shape.y, shape.x

                    # Check if TomTom API Key is present
                    if settings.TOMTOM_API_KEY:
                        url = (
                            f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?"
                            f"key={settings.TOMTOM_API_KEY}&point={lat},{lon}"
                        )
                        try:
                            resp = await http_client.get(url)
                            resp.raise_for_status()
                            flow_data = resp.json().get("flowSegmentData", {})
                            current_speed = float(flow_data.get("currentSpeed", 35.0))
                            free_flow_speed = float(flow_data.get("freeFlowSpeed", 50.0))
                            road_name = flow_data.get("roadName", f"{zone.name} Main Road")
                        except Exception as err:
                            logger.error("TomTom Traffic API call failed for zone %s: %s", zone.name, err)
                            current_speed, free_flow_speed, road_name = 30.0, 45.0, f"{zone.name} Central St"
                    else:
                        # Fallback baseline when TOMTOM_API_KEY is not configured
                        current_speed, free_flow_speed, road_name = 28.5, 45.0, f"{zone.name} Main Corridor"

                    # Calculate congestion level based on speed ratio
                    ratio = current_speed / max(free_flow_speed, 1.0)
                    if ratio >= 0.85:
                        congestion_level = "free_flow"
                    elif ratio >= 0.65:
                        congestion_level = "light"
                    elif ratio >= 0.45:
                        congestion_level = "moderate"
                    elif ratio >= 0.25:
                        congestion_level = "heavy"
                    else:
                        congestion_level = "standstill"

                    traffic_record = TrafficData(
                        zone_id=zone.id,
                        city_id=city.id,
                        location=point_from_coords(lat, lon),
                        road_name=road_name,
                        current_speed=current_speed,
                        free_flow_speed=free_flow_speed,
                        congestion_level=congestion_level,
                        source="tomtom" if settings.TOMTOM_API_KEY else "system_baseline",
                        recorded_at=datetime.now(timezone.utc),
                    )

                    db.add(traffic_record)
                    records_created += 1

        await db.commit()

    logger.info("ingest_traffic completed | records_created=%d", records_created)
    return f"ingest_traffic: successfully created {records_created} traffic records"


async def ingest_social_mentions(ctx: dict, city_id: str | None = None) -> str:
    """Scrape social media mentions from Twitter/Reddit for city topics.

    Args:
        ctx: ARQ worker context.
        city_id: Optional city UUID string.
    """
    logger.info("ingest_social_mentions called | city_id=%s", city_id)
    # Placeholder — real implementation goes here
    return "ingest_social_mentions: not yet implemented"
