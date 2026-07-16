"""arq background worker settings and task routing."""
import logging

from arq.connections import RedisSettings

from app.config import settings
from app.workers.tasks.ai_tasks import compute_city_mood, embed_content, generate_city_summary
from app.workers.tasks.ingestion_tasks import (
    ingest_news_feeds,
    ingest_social_mentions,
    ingest_traffic,
    ingest_weather,
)
from app.workers.tasks.summary_tasks import assemble_daily_digest

logger = logging.getLogger("chai_sutta.worker")


async def startup(ctx: dict) -> None:
    """Worker startup hook."""
    logger.info("Starting Chai Sutta background worker...")
    ctx["some_state"] = "initialized"


async def shutdown(ctx: dict) -> None:
    """Worker shutdown hook."""
    logger.info("Stopping Chai Sutta background worker...")


# arq worker configuration class
class WorkerSettings:
    """Worker settings class for arq."""
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
    functions = [
        # Ingestion tasks
        ingest_news_feeds,
        ingest_weather,
        ingest_traffic,
        ingest_social_mentions,
        # AI tasks
        generate_city_summary,
        compute_city_mood,
        embed_content,
        # Summary / digest tasks
        assemble_daily_digest,
    ]
    on_startup = startup
    on_shutdown = shutdown
    max_jobs = 10
    job_timeout = 600  # 10 minutes timeout for heavy tasks
