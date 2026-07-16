"""Summary background tasks: daily city digest assembly and distribution."""
from __future__ import annotations

import logging

logger = logging.getLogger("chai_sutta.workers.summary")


async def assemble_daily_digest(ctx: dict, city_id: str | None = None) -> str:
    """Assemble and persist the daily city digest for one or all cities.

    Args:
        ctx: ARQ worker context.
        city_id: Optional UUID string. If None, processes all active cities.

    TODO:
        - Query active cities from DB (or use provided city_id)
        - For each city:
            1. Run generate_city_summary to get latest LLM summary text
            2. Run compute_city_mood to get updated mood score
            3. Collect trending_topics from SocialMention aggregation
            4. Persist / update CitySummary record for the day
            5. (Optional) Send push notifications / webhooks to subscribers
    """
    logger.info("assemble_daily_digest called | city_id=%s", city_id)
    # Placeholder — real implementation goes here
    return f"assemble_daily_digest(city_id={city_id}): not yet implemented"
