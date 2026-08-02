"""Periodic task cron scheduler for ARQ background worker."""
from __future__ import annotations

import logging
from arq.cron import cron

from app.workers.tasks.ai_tasks import assemble_daily_digest
from app.workers.tasks.ingestion_tasks import (
    ingest_news_feeds,
    ingest_social_mentions,
    ingest_traffic,
    ingest_weather,
)

logger = logging.getLogger("chai_sutta.workers.scheduler")

# Define scheduled cron jobs for ARQ worker
CRON_JOBS = [
    # Ingest weather data every 30 minutes
    cron(ingest_weather, minute={0, 30}),
    # Ingest traffic data every 15 minutes
    cron(ingest_traffic, minute={0, 15, 30, 45}),
    # Ingest news feeds every hour on the hour
    cron(ingest_news_feeds, minute=0),
    # Scrape social media mentions every 2 hours
    cron(ingest_social_mentions, hour={0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22}, minute=15),
    # Assemble daily city digests every midnight (00:00 UTC)
    cron(assemble_daily_digest, hour=0, minute=0),
]
