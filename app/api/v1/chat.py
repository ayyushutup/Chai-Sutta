"""Ask Tapri chat routes: AI-powered city assistant backed by Gemini."""
from __future__ import annotations

import logging
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_current_user_optional, get_db
from app.config import settings
from app.models.city_summary import CitySummary
from app.models.interaction import UserInteraction
from app.models.news import NewsArticle
from app.models.weather import WeatherData
from app.schemas.chat import ChatRequest, ChatResponse

logger = logging.getLogger("chai_sutta.chat")

router = APIRouter()


# ── Helpers ──────────────────────────────────────────────────────────────────


async def _build_city_context(city_id: UUID, db: AsyncSession) -> str:
    """Collect recent city data to inject as context into the LLM prompt."""
    parts: list[str] = []

    # Latest weather
    weather_result = await db.execute(
        select(WeatherData)
        .where(WeatherData.city_id == city_id)
        .order_by(WeatherData.recorded_at.desc())
        .limit(1)
    )
    weather = weather_result.scalar_one_or_none()
    if weather:
        parts.append(
            f"Current weather: {weather.condition}, {weather.temperature}°C, "
            f"humidity {weather.humidity}%, wind {weather.wind_speed} km/h."
        )

    # Latest city summary / mood
    summary_result = await db.execute(
        select(CitySummary)
        .where(CitySummary.city_id == city_id)
        .order_by(CitySummary.generated_at.desc())
        .limit(1)
    )
    city_summary = summary_result.scalar_one_or_none()
    if city_summary:
        parts.append(f"City mood: {city_summary.mood} (score: {city_summary.mood_score}/100).")
        parts.append(f"Latest city summary: {city_summary.summary_text[:500]}")

    # Top 3 recent news headlines
    news_result = await db.execute(
        select(NewsArticle)
        .where(NewsArticle.city_id == city_id, NewsArticle.status == "published")
        .order_by(NewsArticle.published_at.desc())
        .limit(3)
    )
    headlines = news_result.scalars().all()
    if headlines:
        headline_text = "\n".join(f"- {a.title}" for a in headlines)
        parts.append(f"Recent news headlines:\n{headline_text}")

    return "\n\n".join(parts) if parts else "No recent city data available."


async def _call_gemini(user_message: str, context: str) -> str:
    """Call the Google Gemini API and return the model's reply text."""
    try:
        import google.generativeai as genai  # type: ignore

        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        system_prompt = (
            "You are Tapri, a friendly and knowledgeable AI assistant for hyperlocal "
            "city intelligence in Indian cities. You have access to real-time data about "
            "news, weather, traffic, trains, and community reports. "
            "Answer the user's question helpfully and concisely, referencing the city "
            "context provided. If you don't know something, say so honestly.\n\n"
            f"City context:\n{context}"
        )

        response = model.generate_content(
            [system_prompt, f"User: {user_message}"],
        )
        return response.text

    except ImportError:
        logger.warning("google-generativeai not installed; returning fallback response.")
        return (
            "Tapri is temporarily unavailable (LLM library not installed). "
            "Please check back soon!"
        )
    except Exception as exc:
        logger.error("Gemini API call failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Tapri is temporarily unavailable. Please try again later.",
        )


# ── Endpoints ────────────────────────────────────────────────────────────────


@router.post(
    "/",
    response_model=ChatResponse,
    summary="Ask Tapri a question",
)
async def ask_tapri(
    payload: ChatRequest,
    current_user=Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Ask the Tapri AI assistant a question about the city.

    Authentication is optional — anonymous users get the same response.
    Requires ``GEMINI_API_KEY`` to be set in the environment.
    """
    if not settings.GEMINI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Ask Tapri is not configured (missing GEMINI_API_KEY).",
        )

    # Build city context if city_id provided
    context = ""
    if payload.city_id:
        context = await _build_city_context(payload.city_id, db)

    # Call LLM
    reply = await _call_gemini(payload.message, context)

    # Persist interaction for authenticated users
    if current_user:
        interaction = UserInteraction(
            user_id=current_user.id,
            entity_type="chat",
            entity_id=current_user.id,  # self-reference; no chat entity UUID
            action="ask",
        )
        db.add(interaction)
        await db.commit()

    return ChatResponse(
        reply=reply,
        sources=[{"type": "city_context", "city_id": str(payload.city_id)}] if payload.city_id else [],
        suggested_followups=[
            "What's the weather like?",
            "Any traffic issues?",
            "What's happening in the city today?",
        ],
    )


@router.get(
    "/history",
    response_model=list[dict],
    summary="Get chat history",
)
async def get_chat_history(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get the authenticated user's chat interaction history.

    Returns lightweight interaction records (entity_type='chat', action='ask').
    Full message content persistence is a future enhancement requiring a dedicated
    ChatMessage model.
    """
    stmt = (
        select(UserInteraction)
        .where(
            UserInteraction.user_id == current_user.id,
            UserInteraction.entity_type == "chat",
            UserInteraction.action == "ask",
        )
        .order_by(UserInteraction.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    interactions = result.scalars().all()

    return [
        {
            "id": str(i.id),
            "action": i.action,
            "created_at": i.created_at.isoformat() if i.created_at else None,
        }
        for i in interactions
    ]
