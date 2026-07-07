"""Database seed script to populate development data."""
import asyncio
import logging
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import settings
from app.models.city import City
from app.models.zone import Zone
from app.models.user import User
from app.models.report import CommunityReport
from app.core.security import hash_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("chai_sutta.seed")


async def seed_data(session: AsyncSession) -> None:
    # 1. Clean existing records to make seeding repeatable
    logger.info("Cleaning existing data...")
    await session.execute(delete(CommunityReport))
    await session.execute(delete(User))
    await session.execute(delete(Zone))
    await session.execute(delete(City))
    await session.commit()

    # 2. Add Cities
    logger.info("Seeding cities...")
    bengaluru = City(
        name="Bengaluru",
        slug="bengaluru",
        boundary="SRID=4326;POLYGON((77.45 12.85, 77.75 12.85, 77.75 13.10, 77.45 13.10, 77.45 12.85))",
        metadata_={"state": "Karnataka", "country": "India"},
    )
    mumbai = City(
        name="Mumbai",
        slug="mumbai",
        boundary="SRID=4326;POLYGON((72.75 18.85, 73.05 18.85, 73.05 19.30, 72.75 19.30, 72.75 18.85))",
        metadata_={"state": "Maharashtra", "country": "India"},
    )
    session.add_all([bengaluru, mumbai])
    await session.flush()  # populated IDs

    # 3. Add Zones
    logger.info("Seeding zones...")
    indiranagar = Zone(
        city_id=bengaluru.id,
        name="Indiranagar",
        slug="indiranagar",
        boundary="SRID=4326;POLYGON((77.62 12.96, 77.66 12.96, 77.66 12.99, 77.62 12.99, 77.62 12.96))",
        centroid="SRID=4326;POINT(77.6412 12.9719)",
        zone_type="neighborhood",
    )
    koramangala = Zone(
        city_id=bengaluru.id,
        name="Koramangala",
        slug="koramangala",
        boundary="SRID=4326;POLYGON((77.60 12.92, 77.64 12.92, 77.64 12.95, 77.60 12.95, 77.60 12.92))",
        centroid="SRID=4326;POINT(77.6245 12.9352)",
        zone_type="neighborhood",
    )
    bandra = Zone(
        city_id=mumbai.id,
        name="Bandra West",
        slug="bandra-west",
        boundary="SRID=4326;POLYGON((72.81 19.04, 72.85 19.04, 72.85 19.08, 72.81 19.08, 72.81 19.04))",
        centroid="SRID=4326;POINT(72.8402 19.0596)",
        zone_type="neighborhood",
    )
    session.add_all([indiranagar, koramangala, bandra])
    await session.flush()

    # 4. Add Users
    logger.info("Seeding users...")
    admin = User(
        email="admin@chaisutta.com",
        display_name="Chai Admin",
        password_hash=hash_password("adminpassword123"),
        auth_provider="email",
        home_zone_id=indiranagar.id,
        reputation_score=100,
    )
    user1 = User(
        email="ayush@chaisutta.com",
        display_name="Ayush Thakur",
        password_hash=hash_password("userpassword123"),
        auth_provider="email",
        home_zone_id=koramangala.id,
        reputation_score=50,
    )
    session.add_all([admin, user1])
    await session.flush()

    # 5. Add Community Reports
    logger.info("Seeding community reports...")
    report1 = CommunityReport(
        user_id=user1.id,
        city_id=bengaluru.id,
        zone_id=indiranagar.id,
        category="traffic",
        severity="high",
        content="Heavy Traffic near 100ft Road: Gridlock traffic starting from Indiranagar metro station towards Domlur. Avoid this route.",
        location="SRID=4326;POINT(77.6415 12.9725)",
        upvotes=5,
        downvotes=0,
        verification_status="verified",
    )
    report2 = CommunityReport(
        user_id=user1.id,
        city_id=bengaluru.id,
        zone_id=koramangala.id,
        category="utility",
        severity="medium",
        content="Waterlogging in Koramangala 4th Block: Substantial water pooling on the main road after short rain showers. Drive carefully.",
        location="SRID=4326;POINT(77.6250 12.9360)",
        upvotes=3,
        downvotes=1,
        verification_status="unverified",
    )
    report3 = CommunityReport(
        user_id=admin.id,
        city_id=mumbai.id,
        zone_id=bandra.id,
        category="safety",
        severity="low",
        content="Streetlights out near Carter Road: Several lampposts are dark along the promenade. Reported to municipal authorities.",
        location="SRID=4326;POINT(72.8398 19.0602)",
        upvotes=1,
        downvotes=0,
        verification_status="verified",
    )
    session.add_all([report1, report2, report3])
    await session.commit()
    logger.info("Database seeding completed successfully!")


async def main():
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        await seed_data(session)
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
