"""Redis client with connection pooling and cache utilities."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

import redis.asyncio as redis
from redis.asyncio import ConnectionPool, Redis

from app.config import settings


class RedisManager:
    """Manages Redis connections with pooling and cache-aside pattern support."""

    def __init__(self) -> None:
        self._pool: ConnectionPool | None = None
        self._client: Redis | None = None

    async def connect(self, url: str | None = None) -> None:
        """Create a connection pool and Redis client."""
        redis_url = url or settings.REDIS_URL
        self._pool = ConnectionPool.from_url(
            redis_url,
            max_connections=20,
            decode_responses=True,
        )
        self._client = Redis(connection_pool=self._pool)
        # Verify connectivity
        await self._client.ping()

    async def disconnect(self) -> None:
        """Close the Redis client and connection pool."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None
        if self._pool is not None:
            await self._pool.disconnect()
            self._pool = None

    @property
    def client(self) -> Redis:
        """Return the Redis client instance."""
        if self._client is None:
            raise RuntimeError("Redis not connected. Call connect() first.")
        return self._client

    async def get_cached(self, key: str) -> str | None:
        """Get a cached value by key."""
        return await self.client.get(key)

    async def set_cached(
        self, key: str, value: str, ttl_seconds: int = 300
    ) -> None:
        """Set a cached value with TTL (default 5 minutes)."""
        await self.client.set(key, value, ex=ttl_seconds)

    async def delete_cached(self, key: str) -> None:
        """Delete a cached key."""
        await self.client.delete(key)

    async def get_or_set(
        self,
        key: str,
        ttl_seconds: int,
        factory_fn: Callable[[], Awaitable[str]],
    ) -> str:
        """Cache-aside pattern: get from cache or compute and store.

        If the key exists in cache, return the cached value.
        Otherwise, call factory_fn to compute the value, cache it, and return.
        """
        cached = await self.get_cached(key)
        if cached is not None:
            return cached

        value = await factory_fn()
        await self.set_cached(key, value, ttl_seconds)
        return value

    async def increment(self, key: str, ttl: int = 60) -> int:
        """Increment a counter key (useful for rate limiting).

        Creates the key if it doesn't exist and sets a TTL on first creation.
        Returns the new count.
        """
        pipe = self.client.pipeline()
        pipe.incr(key)
        pipe.expire(key, ttl, nx=True)
        results = await pipe.execute()
        return results[0]  # The INCR result


# Global singleton instance
redis_manager = RedisManager()


async def get_redis() -> Redis:
    """FastAPI dependency that returns the Redis client."""
    return redis_manager.client
