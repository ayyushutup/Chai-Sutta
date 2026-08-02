"""Integration tests for community reports API endpoints."""
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_list_community_reports(client: AsyncClient):
    """Test listing community reports."""
    response = await client.get("/api/v1/reports/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data

@pytest.mark.asyncio
async def test_get_nonexistent_report(client: AsyncClient):
    """Test retrieving non-existent community report."""
    response = await client.get("/api/v1/reports/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
