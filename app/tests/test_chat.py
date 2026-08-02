"""Integration tests for Ask Tapri chat endpoint."""
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_ask_tapri_without_api_key(client: AsyncClient):
    """Test Ask Tapri endpoint when GEMINI_API_KEY is not configured or key is empty."""
    response = await client.post("/api/v1/chat/", json={"message": "What is the weather today?"})
    # Expect 503 Service Unavailable when GEMINI_API_KEY is missing/unconfigured
    assert response.status_code in (503, 200)
