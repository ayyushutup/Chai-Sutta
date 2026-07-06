"""File storage abstraction with local filesystem backend."""
from __future__ import annotations

import os
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from uuid import uuid4

import aiofiles
from fastapi import UploadFile

from app.config import settings


class StorageBackend(ABC):
    """Abstract base class for file storage backends."""

    @abstractmethod
    async def upload_file(self, file: UploadFile, subpath: str = "") -> str:
        """Upload a file and return its storage path.

        Args:
            file: FastAPI UploadFile object.
            subpath: Optional subdirectory within the storage root.

        Returns:
            Relative path to the stored file.
        """
        ...

    @abstractmethod
    async def delete_file(self, path: str) -> None:
        """Delete a file by its storage path.

        Args:
            path: Relative path to the file.
        """
        ...

    @abstractmethod
    def get_url(self, path: str) -> str:
        """Get the public URL for a stored file.

        Args:
            path: Relative path to the file.

        Returns:
            URL string to access the file.
        """
        ...


class LocalStorage(StorageBackend):
    """Local filesystem storage backend."""

    def __init__(self, base_path: str | None = None) -> None:
        self.base_path = Path(base_path or settings.LOCAL_STORAGE_PATH)
        self.base_path.mkdir(parents=True, exist_ok=True)

    async def upload_file(self, file: UploadFile, subpath: str = "") -> str:
        """Save an uploaded file to the local filesystem.

        Generates a unique filename to prevent collisions.

        Args:
            file: FastAPI UploadFile object.
            subpath: Optional subdirectory (e.g., 'reports', 'avatars').

        Returns:
            Relative path from storage root to the saved file.
        """
        # Build target directory
        target_dir = self.base_path / subpath if subpath else self.base_path
        target_dir.mkdir(parents=True, exist_ok=True)

        # Generate unique filename preserving extension
        ext = ""
        if file.filename:
            ext = Path(file.filename).suffix
        unique_name = f"{uuid4().hex}{ext}"
        target_path = target_dir / unique_name

        # Write file asynchronously
        async with aiofiles.open(target_path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)

        # Return relative path
        return str(target_path.relative_to(self.base_path))

    async def delete_file(self, path: str) -> None:
        """Delete a file from the local filesystem.

        Args:
            path: Relative path from storage root.
        """
        full_path = self.base_path / path
        if full_path.exists():
            full_path.unlink()

    def get_url(self, path: str) -> str:
        """Get the URL path for a locally stored file.

        Args:
            path: Relative path from storage root.

        Returns:
            URL path (e.g., /uploads/reports/abc123.jpg).
        """
        return f"/uploads/{path}"


def get_storage() -> StorageBackend:
    """Factory function to get the configured storage backend.

    Returns:
        StorageBackend instance based on settings.STORAGE_BACKEND.
    """
    if settings.STORAGE_BACKEND == "local":
        return LocalStorage()
    # Future: add S3, GCS backends here
    raise ValueError(f"Unknown storage backend: {settings.STORAGE_BACKEND}")
