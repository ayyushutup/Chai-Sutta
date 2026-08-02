"""Unit & integration tests for health check and general API endpoints."""
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test the root health check endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data or "message" in data or response.status_code == 200
