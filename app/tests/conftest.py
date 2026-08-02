"""Test configuration and fixtures for Chai Sutta pytest suite."""
import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Yield an async test HTTP client targeting the FastAPI application."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver"
    ) as ac:
        yield ac
