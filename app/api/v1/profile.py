"""Profile routes: user profile management, reports, and bookmarks."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.report import CommunityReport
from app.models.user import User
from app.schemas.user import UserResponse
from pydantic import BaseModel, EmailStr, Field

router = APIRouter()


# ── Schemas ─────────────────────────────────────────────────────────────────


class ProfileUpdate(BaseModel):
    """Schema for updating user profile."""
    display_name: str | None = Field(default=None, min_length=2, max_length=100)
    avatar_url: str | None = None
    home_zone_id: UUID | None = None


class ReportSummary(BaseModel):
    """Simplified report summary for profile listing."""
    id: UUID
    category: str
    content: str
    verification_status: str
    upvotes: int = 0
    downvotes: int = 0

    model_config = {"from_attributes": True}


# ── Endpoints ───────────────────────────────────────────────────────────────


@router.get(
    "/",
    response_model=UserResponse,
    summary="Get own profile",
)
async def get_profile(
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get the authenticated user's profile."""
    return UserResponse.model_validate(current_user)


@router.put(
    "/",
    response_model=UserResponse,
    summary="Update profile",
)
async def update_profile(
    payload: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Update the authenticated user's profile fields."""
    if payload.display_name is not None:
        current_user.display_name = payload.display_name
    if payload.avatar_url is not None:
        current_user.avatar_url = payload.avatar_url
    if payload.home_zone_id is not None:
        current_user.home_zone_id = payload.home_zone_id

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return UserResponse.model_validate(current_user)


@router.get(
    "/reports",
    response_model=list[ReportSummary],
    summary="Get own reports",
)
async def get_my_reports(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get reports created by the authenticated user, newest first."""
    stmt = (
        select(CommunityReport)
        .where(CommunityReport.user_id == current_user.id, CommunityReport.is_active == True)
        .order_by(CommunityReport.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    reports = result.scalars().all()
    return [ReportSummary.model_validate(r) for r in reports]


@router.get(
    "/bookmarks",
    response_model=list[dict],
    summary="Get bookmarked items",
)
async def get_bookmarks(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get the authenticated user's bookmarked items.

    Bookmarks are stored as UserInteraction records with action='bookmark'.
    Returns the raw interaction records; full entity hydration is a future enhancement.
    """
    from app.models.interaction import UserInteraction

    stmt = (
        select(UserInteraction)
        .where(
            UserInteraction.user_id == current_user.id,
            UserInteraction.action == "bookmark",
        )
        .order_by(UserInteraction.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    interactions = result.scalars().all()

    return [
        {
            "id": str(i.id),
            "entity_type": i.entity_type,
            "entity_id": str(i.entity_id),
            "bookmarked_at": i.created_at.isoformat() if i.created_at else None,
        }
        for i in interactions
    ]
