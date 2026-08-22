"""Integration tests for social media ingestion tasks."""
import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy import select, delete
from app.models.social_mention import SocialMention
from app.models.zone import Zone
from app.workers.tasks.ingestion_tasks import ingest_social_mentions
from app.core.database import init_db, close_db
import app.core.database as db_mod

@pytest.mark.asyncio
async def test_ingest_social_mentions_reddit():
    """Test parsing, mapping, and saving of scraped Reddit posts."""
    
    mock_reddit_response = {
        "kind": "Listing",
        "data": {
            "children": [
                {
                    "kind": "t3",
                    "data": {
                        "id": "mock_post_1",
                        "title": "Stuck in massive traffic at Indiranagar 100ft road!",
                        "selftext": "Avoid this road if you can.",
                        "author": "traffic_watcher",
                        "score": 42,
                        "created_utc": 1672531199.0
                    }
                },
                {
                    "kind": "t3",
                    "data": {
                        "id": "mock_post_2",
                        "title": "Nice weather in Koramangala today",
                        "selftext": "Sunny with light breeze.",
                        "author": "weather_fan",
                        "score": 10,
                        "created_utc": 1672531200.0
                    }
                }
            ]
        }
    }

    from unittest.mock import MagicMock
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_reddit_response
    mock_response.raise_for_status = MagicMock()

    ctx = {
        "db_session_factory": db_mod.async_session_factory
    }

    # Clean existing test mentions if any to make test repeatable
    async with db_mod.async_session_factory() as session:
        await session.execute(delete(SocialMention).where(SocialMention.post_id.in_(["mock_post_1", "mock_post_2"])))
        await session.commit()

    with patch("httpx.AsyncClient.get", return_value=mock_response) as mock_get:
        # Run ingestion
        result = await ingest_social_mentions(ctx)
        
        assert "successfully created" in result
        
        # Verify db contains correct records
        async with db_mod.async_session_factory() as session:
            stmt = select(SocialMention).where(SocialMention.platform == "reddit")
            res = await session.execute(stmt)
            mentions = res.scalars().all()
            
            # Filter for our mock posts
            mock_mentions = [m for m in mentions if m.post_id in ["mock_post_1", "mock_post_2"]]
            assert len(mock_mentions) == 2
            
            # Check Indiranagar mapping
            m1 = next(m for m in mock_mentions if m.post_id == "mock_post_1")
            assert m1.category == "traffic"
            assert m1.zone_id is not None
            
            # Verify the zone_id matches Indiranagar
            zone_res = await session.execute(select(Zone).where(Zone.name == "Indiranagar"))
            indiranagar_zone = zone_res.scalar_one_or_none()
            assert indiranagar_zone is not None
            assert m1.zone_id == indiranagar_zone.id
            
            # Check Koramangala mapping
            m2 = next(m for m in mock_mentions if m.post_id == "mock_post_2")
            assert m2.category == "weather"
            assert m2.zone_id is not None
            
            # Verify the zone_id matches Koramangala
            zone_res = await session.execute(select(Zone).where(Zone.name == "Koramangala"))
            koramangala_zone = zone_res.scalar_one_or_none()
            assert koramangala_zone is not None
            assert m2.zone_id == koramangala_zone.id
            
            # Clean up after test
            await session.execute(delete(SocialMention).where(SocialMention.post_id.in_(["mock_post_1", "mock_post_2"])))
            await session.commit()
