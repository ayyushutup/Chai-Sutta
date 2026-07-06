"""Chai Sutta FastAPI application factory and lifespan management."""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.core.database import init_db, close_db
from app.core.exceptions import register_exception_handlers
from app.core.middleware import RequestLoggingMiddleware
from app.core.qdrant import qdrant_manager
from app.core.redis import redis_manager

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.APP_DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("chai_sutta")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan manager.

    Initializes and cleanly shuts down:
    - Database engine (async SQLAlchemy)
    - Redis client (connection pool)
    - Qdrant vector DB client
    """
    logger.info("Starting Chai Sutta API [%s]", settings.APP_ENV)

    # Startup
    await init_db()
    logger.info("Database engine initialized")

    try:
        await redis_manager.connect()
        logger.info("Redis connected")
    except Exception as e:
        logger.warning("Redis connection failed (non-fatal): %s", e)

    try:
        await qdrant_manager.init()
        logger.info("Qdrant client initialized")
    except Exception as e:
        logger.warning("Qdrant connection failed (non-fatal): %s", e)

    yield

    # Shutdown
    logger.info("Shutting down Chai Sutta API...")
    await qdrant_manager.close()
    await redis_manager.disconnect()
    await close_db()
    logger.info("All connections closed. Goodbye!")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Chai Sutta API",
        description=(
            "Hyperlocal city intelligence platform — real-time news, weather, "
            "traffic, events, community reports, and AI-powered city insights."
        ),
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS middleware — allow all origins in development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.APP_DEBUG else [],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Request logging middleware
    app.add_middleware(RequestLoggingMiddleware)

    # Register custom exception handlers
    register_exception_handlers(app)

    # Include the v1 API router
    from app.api.v1.router import api_router
    app.include_router(api_router)

    @app.get("/", tags=["Health"])
    async def root():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "service": "Chai Sutta API",
            "version": "0.1.0",
            "environment": settings.APP_ENV,
        }

    return app


# Application instance
app = create_app()
