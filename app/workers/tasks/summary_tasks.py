"""Summary background tasks: daily city digest assembly and distribution."""
from __future__ import annotations

import logging
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.models.city import City
from app.workers.tasks.ai_tasks import generate_city_summary

logger = logging.getLogger("chai_sutta.workers.summary")


def _create_db_session_factory() -> async_sessionmaker[AsyncSession]:
    """Helper to create DB session factory for worker tasks if not provided in ctx."""
    engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)
    return async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def assemble_daily_digest(ctx: dict, city_id: str | None = None) -> str:
    """Assemble and persist the daily city digest for one or all active cities.

    Args:
        ctx: ARQ worker context.
        city_id: Optional UUID string. If None, processes all active cities.
    """
    logger.info("assemble_daily_digest starting | city_id=%s", city_id)

    session_factory = ctx.get("db_session_factory")
    if not session_factory:
        session_factory = _create_db_session_factory()

    processed_count = 0

    async with session_factory() as db:
        stmt = select(City).where(City.is_active == True)
        if city_id:
            stmt = stmt.where(City.id == UUID(city_id))

        result = await db.execute(stmt)
        cities = result.scalars().all()

        for city in cities:
            try:
                await generate_city_summary(ctx, str(city.id))
                processed_count += 1
            except Exception as err:
                logger.error("Failed to assemble daily digest for city %s (%s): %s", city.name, city.id, err)

    logger.info("assemble_daily_digest completed | cities_processed=%d", processed_count)
    return f"assemble_daily_digest: successfully processed digests for {processed_count} cities"
