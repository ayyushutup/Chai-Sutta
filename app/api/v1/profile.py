"""Profile routes: user profile management, reports, and bookmarks."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db

router = APIRouter()


# ── Schemas ─────────────────────────────────────────────────────────────────


class UserResponse(BaseModel):
    """User profile response."""
    id: UUID
    email: str
    display_name: str
    avatar_url: str | None = None
    city_id: UUID | None = None
    bio: str | None = None
    report_count: int = 0
    is_active: bool = True

    model_config = {"from_attributes": True}


class ProfileUpdate(BaseModel):
    """Schema for updating user profile."""
    display_name: str | None = Field(default=None, min_length=2, max_length=100)
    bio: str | None = Field(default=None, max_length=500)
    avatar_url: str | None = None
    city_id: UUID | None = None


class ReportResponse(BaseModel):
    """Simplified report response for profile listing."""
    id: UUID
    title: str
    category: str
    status: str
    upvotes: int = 0
    created_at: str | None = None

    model_config = {"from_attributes": True}


class BookmarkResponse(BaseModel):
    """Bookmarked item."""
    id: UUID
    content_type: str  # news, event, report
    content_id: UUID
    title: str
    bookmarked_at: str | None = None


# ── Endpoints ───────────────────────────────────────────────────────────────


@router.get(
    "/",
    response_model=UserResponse,
    summary="Get own profile",
)
async def get_profile(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get the authenticated user's profile."""
    return current_user


@router.put(
    "/",
    response_model=UserResponse,
    summary="Update profile",
)
async def update_profile(
    payload: ProfileUpdate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Update the authenticated user's profile."""
    # TODO: Implement profile update service
    raise NotImplementedError("Profile update not yet implemented.")


@router.get(
    "/reports",
    response_model=list[ReportResponse],
    summary="Get own reports",
)
async def get_my_reports(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get reports created by the authenticated user."""
    # TODO: Implement user reports service
    return []


@router.get(
    "/bookmarks",
    response_model=list[BookmarkResponse],
    summary="Get bookmarked items",
)
async def get_bookmarks(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get the authenticated user's bookmarked items."""
    # TODO: Implement bookmarks service
    return []
