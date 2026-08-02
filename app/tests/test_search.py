"""Integration tests for search and autocomplete API endpoints."""
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_search_content(client: AsyncClient):
    """Test full-text search query across content."""
    response = await client.get("/api/v1/search/", params={"q": "traffic"})
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "query" in data
    assert data["query"] == "traffic"

@pytest.mark.asyncio
async def test_search_suggest_autocomplete(client: AsyncClient):
    """Test autocomplete search suggestion endpoint."""
    response = await client.get("/api/v1/search/suggest", params={"q": "bengaluru"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
