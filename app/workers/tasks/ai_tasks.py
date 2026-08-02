"""AI background tasks: LLM city summaries, mood scoring, and content embedding."""
from __future__ import annotations

from datetime import datetime, timezone
import json
import logging
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.models.city import City
from app.models.city_summary import CitySummary
from app.models.event import Event
from app.models.news import NewsArticle
from app.models.report import CommunityReport
from app.models.traffic import TrafficData
from app.models.weather import WeatherData

logger = logging.getLogger("chai_sutta.workers.ai")


def _create_db_session_factory() -> async_sessionmaker[AsyncSession]:
    """Helper to create DB session factory for worker tasks if not provided in ctx."""
    engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)
    return async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def _gather_city_data(db: AsyncSession, city_id_uuid: UUID) -> dict:
    """Collect recent city intelligence data for LLM context."""
    # 1. Fetch City details
    city_res = await db.execute(select(City).where(City.id == city_id_uuid))
    city = city_res.scalar_one_or_none()
    city_name = city.name if city else "Unknown City"

    # 2. Fetch Weather
    weather_res = await db.execute(
        select(WeatherData)
        .where(WeatherData.city_id == city_id_uuid)
        .order_by(WeatherData.recorded_at.desc())
        .limit(1)
    )
    weather = weather_res.scalar_one_or_none()
    weather_info = {
        "condition": weather.condition if weather else "N/A",
        "temperature": weather.temperature if weather else 0.0,
        "humidity": weather.humidity if weather else 0.0,
        "wind_speed": weather.wind_speed if weather else 0.0,
    }

    # 3. Fetch Top News Articles
    news_res = await db.execute(
        select(NewsArticle)
        .where(NewsArticle.city_id == city_id_uuid, NewsArticle.status == "published")
        .order_by(NewsArticle.published_at.desc())
        .limit(5)
    )
    news_items = [{"title": n.title, "summary": n.summary or n.title} for n in news_res.scalars().all()]

    # 4. Fetch Active Community Reports
    reports_res = await db.execute(
        select(CommunityReport)
        .where(CommunityReport.city_id == city_id_uuid, CommunityReport.is_active == True)
        .order_by(CommunityReport.created_at.desc())
        .limit(5)
    )
    report_items = [{"category": r.category, "content": r.content} for r in reports_res.scalars().all()]

    # 5. Fetch Traffic Incidents / Congestion
    traffic_res = await db.execute(
        select(TrafficData)
        .where(TrafficData.city_id == city_id_uuid)
        .order_by(TrafficData.recorded_at.desc())
        .limit(5)
    )
    traffic_items = [
        {"road_name": t.road_name, "congestion": t.congestion_level, "speed": t.current_speed}
        for t in traffic_res.scalars().all()
    ]

    return {
        "city_name": city_name,
        "weather": weather_info,
        "news": news_items,
        "reports": report_items,
        "traffic": traffic_items,
    }


async def generate_city_summary(ctx: dict, city_id: str) -> str:
    """Generate an AI city summary for the given city using Gemini LLM.

    Args:
        ctx: ARQ worker context.
        city_id: UUID string of the city to summarise.
    """
    logger.info("generate_city_summary starting | city_id=%s", city_id)

    if not settings.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY is not configured; skipping city summary generation.")
        return f"generate_city_summary({city_id}): skipped (missing GEMINI_API_KEY)"

    session_factory = ctx.get("db_session_factory")
    if not session_factory:
        session_factory = _create_db_session_factory()

    city_id_uuid = UUID(city_id)

    async with session_factory() as db:
        city_data = await _gather_city_data(db, city_id_uuid)

        # Build prompt for JSON formatted output
        prompt = f"""
You are the AI city intelligence engine for "{city_data['city_name']}".
Synthesize the following real-time city snapshot into a structured JSON summary:

CITY SNAPSHOT:
- Weather: {city_data['weather']}
- Top News: {json.dumps(city_data['news'])}
- User Incident Reports: {json.dumps(city_data['reports'])}
- Traffic Conditions: {json.dumps(city_data['traffic'])}

Please reply ONLY with a valid JSON object with the following schema:
{{
  "summary_text": "A cohesive 2-3 paragraph summary of current city events, weather, and traffic.",
  "mood": "Overall city mood label (one of: calm, active, tense, festive, busy, chaotic)",
  "mood_score": integer between 0 and 100,
  "mood_emoji": "single emoji reflecting mood",
  "trending_topics": ["topic1", "topic2", "topic3"]
}}
"""

        try:
            import google.generativeai as genai

            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")

            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"},
            )

            result_json = json.loads(response.text)

            summary_text = result_json.get("summary_text", "City updates synthesized.")
            mood = result_json.get("mood", "active")
            mood_score = int(result_json.get("mood_score", 70))
            mood_emoji = result_json.get("mood_emoji", "🌆")
            trending_topics = result_json.get("trending_topics", [])

        except Exception as err:
            logger.error("Failed to generate city summary via Gemini for city %s: %s", city_id, err)
            # Fallback summary if LLM call fails
            summary_text = (
                f"Current conditions in {city_data['city_name']}: "
                f"Weather is {city_data['weather']['condition']} at {city_data['weather']['temperature']}°C. "
                f"News and community reports are being tracked in real-time."
            )
            mood = "active"
            mood_score = 65
            mood_emoji = "🏙️"
            trending_topics = ["city_life", "weather", "updates"]

        # Save to DB
        summary_record = CitySummary(
            city_id=city_id_uuid,
            summary_text=summary_text,
            mood=mood,
            mood_score=mood_score,
            mood_emoji=mood_emoji,
            data_snapshot=city_data,
            trending_topics={"topics": trending_topics},
            generated_at=datetime.now(timezone.utc),
        )

        db.add(summary_record)
        await db.commit()

    logger.info("generate_city_summary completed for city %s", city_id)
    return f"generate_city_summary({city_id}): successfully created summary record"


async def compute_city_mood(ctx: dict, city_id: str) -> str:
    """Compute the aggregate mood / sentiment score for a city.

    Args:
        ctx: ARQ worker context.
        city_id: UUID string of the city.
    """
    logger.info("compute_city_mood called | city_id=%s", city_id)
    # Delegates to generate_city_summary as mood calculation is included in summary synthesis
    return await generate_city_summary(ctx, city_id)


async def embed_content(ctx: dict, entity_type: str, entity_id: str) -> str:
    """Generate and store a vector embedding for a content entity in Qdrant.

    Args:
        ctx: ARQ worker context.
        entity_type: One of 'news', 'event', 'report'.
        entity_id: UUID string of the entity to embed.
    """
    logger.info("embed_content called | entity_type=%s entity_id=%s", entity_type, entity_id)
    # Placeholder — real implementation goes here
    return f"embed_content({entity_type}, {entity_id}): not yet implemented"
