"""Qdrant vector database client for semantic search."""
from __future__ import annotations

from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

from app.config import settings


class QdrantManager:
    """Manages Qdrant vector DB connections and operations."""

    def __init__(self) -> None:
        self.client: QdrantClient | None = None

    async def init(
        self,
        host: str | None = None,
        port: int | None = None,
    ) -> None:
        """Initialize the Qdrant client.

        Args:
            host: Qdrant server host. Defaults to settings.QDRANT_HOST.
            port: Qdrant server port. Defaults to settings.QDRANT_PORT.
        """
        self.client = QdrantClient(
            host=host or settings.QDRANT_HOST,
            port=port or settings.QDRANT_PORT,
            prefer_grpc=True,
        )

    async def close(self) -> None:
        """Close the Qdrant client connection."""
        if self.client is not None:
            self.client.close()
            self.client = None

    def _ensure_client(self) -> QdrantClient:
        """Ensure client is initialized."""
        if self.client is None:
            raise RuntimeError("Qdrant client not initialized. Call init() first.")
        return self.client

    async def ensure_collection(
        self,
        name: str,
        vector_size: int,
        distance: Distance = Distance.COSINE,
    ) -> None:
        """Create a collection if it doesn't already exist.

        Args:
            name: Collection name.
            vector_size: Dimensionality of the vectors.
            distance: Distance metric (default: cosine similarity).
        """
        client = self._ensure_client()
        collections = client.get_collections().collections
        existing_names = {c.name for c in collections}

        if name not in existing_names:
            client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=distance,
                ),
            )

    async def upsert_points(
        self,
        collection: str,
        points: list[dict[str, Any]],
    ) -> None:
        """Upsert points into a collection.

        Args:
            collection: Collection name.
            points: List of dicts with keys: id, vector, payload.
        """
        client = self._ensure_client()
        point_structs = [
            PointStruct(
                id=p["id"],
                vector=p["vector"],
                payload=p.get("payload", {}),
            )
            for p in points
        ]
        client.upsert(
            collection_name=collection,
            points=point_structs,
        )

    async def search(
        self,
        collection: str,
        query_vector: list[float],
        filters: dict[str, Any] | None = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """Search for similar vectors in a collection.

        Args:
            collection: Collection name.
            query_vector: Query embedding vector.
            filters: Optional filter conditions as {field: value}.
            limit: Maximum number of results.

        Returns:
            List of dicts with id, score, and payload.
        """
        client = self._ensure_client()

        # Build Qdrant filter from dict
        qdrant_filter = None
        if filters:
            conditions = [
                FieldCondition(key=k, match=MatchValue(value=v))
                for k, v in filters.items()
            ]
            qdrant_filter = Filter(must=conditions)

        results = client.search(
            collection_name=collection,
            query_vector=query_vector,
            query_filter=qdrant_filter,
            limit=limit,
        )

        return [
            {
                "id": hit.id,
                "score": hit.score,
                "payload": hit.payload,
            }
            for hit in results
        ]

    async def delete_points(
        self,
        collection: str,
        ids: list[str | int],
    ) -> None:
        """Delete points from a collection by ID.

        Args:
            collection: Collection name.
            ids: List of point IDs to delete.
        """
        client = self._ensure_client()
        from qdrant_client.models import PointIdsList

        client.delete(
            collection_name=collection,
            points_selector=PointIdsList(points=ids),
        )


# Global singleton instance
qdrant_manager = QdrantManager()
