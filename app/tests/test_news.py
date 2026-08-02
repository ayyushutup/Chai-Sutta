"""Integration tests for news API endpoints."""
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_list_news_articles(client: AsyncClient):
    """Test listing news articles with default pagination."""
    response = await client.get("/api/v1/news/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data

@pytest.mark.asyncio
async def test_get_nonexistent_news_article(client: AsyncClient):
    """Test getting a single news article with invalid/random UUID."""
    response = await client.get("/api/v1/news/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
