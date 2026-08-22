"""Test configuration and fixtures for Chai Sutta pytest suite."""
import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from app.main import app

from app.core.database import init_db, close_db

@pytest.fixture(autouse=True)
async def initialize_test_db():
    """Initialize database before running tests and close after."""
    await init_db()
    yield
    await close_db()

@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Yield an async test HTTP client targeting the FastAPI application."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver"
    ) as ac:
        yield ac
