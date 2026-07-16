"""AI background tasks: LLM city summaries, mood scoring, and content embedding."""
from __future__ import annotations

import logging

logger = logging.getLogger("chai_sutta.workers.ai")


async def generate_city_summary(ctx: dict, city_id: str) -> str:
    """Generate an AI city summary for the given city using Gemini / Groq.

    Args:
        ctx: ARQ worker context.
        city_id: UUID string of the city to summarise.

    TODO:
        - Query recent news, weather, traffic, and social mentions for city_id
        - Build a structured prompt with the collected data
        - Call Gemini (settings.GEMINI_API_KEY) or Groq (settings.GROQ_API_KEY)
        - Parse the response and persist a CitySummary record with generated_at=NOW()
        - Update mood, mood_score, mood_emoji, and trending_topics fields
    """
    logger.info("generate_city_summary called | city_id=%s", city_id)
    # Placeholder — real implementation goes here
    return f"generate_city_summary({city_id}): not yet implemented"


async def compute_city_mood(ctx: dict, city_id: str) -> str:
    """Compute the aggregate mood / sentiment score for a city.

    Args:
        ctx: ARQ worker context.
        city_id: UUID string of the city.

    TODO:
        - Retrieve recent news articles with ai_metadata.sentiment fields
        - Retrieve recent SocialMention records with ai_metadata.sentiment fields
        - Compute weighted average sentiment score (news 40%, social 60%)
        - Map numeric score to mood label and emoji
        - Upsert into CitySummary (mood, mood_score, mood_emoji, data_snapshot)
    """
    logger.info("compute_city_mood called | city_id=%s", city_id)
    # Placeholder — real implementation goes here
    return f"compute_city_mood({city_id}): not yet implemented"


async def embed_content(ctx: dict, entity_type: str, entity_id: str) -> str:
    """Generate and store a vector embedding for a content entity in Qdrant.

    Args:
        ctx: ARQ worker context.
        entity_type: One of 'news', 'event', 'report'.
        entity_id: UUID string of the entity to embed.

    TODO:
        - Load the entity text (title + summary/content) from Postgres
        - Generate embedding using sentence-transformers (all-MiniLM-L6-v2)
        - Upsert into Qdrant collection '{entity_type}_vectors' with entity_id as point ID
        - Store metadata (city_id, category, published_at) as Qdrant payload
    """
    logger.info("embed_content called | entity_type=%s entity_id=%s", entity_type, entity_id)
    # Placeholder — real implementation goes here
    return f"embed_content({entity_type}, {entity_id}): not yet implemented"
