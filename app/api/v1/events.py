"""Events routes: list, create, detail, and upcoming."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db

router = APIRouter()


# ── Schemas ─────────────────────────────────────────────────────────────────


class EventCreate(BaseModel):
    """Schema for creating an event."""
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=10, max_length=5000)
    city_id: UUID
    zone_id: UUID | None = None
    venue: str | None = None
    address: str | None = None
    lat: float | None = None
    lon: float | None = None
    starts_at: str
    ends_at: str | None = None
    category: str | None = None
    image_url: str | None = None
    ticket_url: str | None = None
    is_free: bool = True


class EventResponse(BaseModel):
    """Event response."""
    id: UUID
    title: str
    description: str
    city_id: UUID
    zone_id: UUID | None = None
    venue: str | None = None
    address: str | None = None
    lat: float | None = None
    lon: float | None = None
    starts_at: str
    ends_at: str | None = None
    category: str | None = None
    image_url: str | None = None
    ticket_url: str | None = None
    is_free: bool = True
    created_by: UUID | None = None
    created_at: str | None = None

    model_config = {"from_attributes": True}


class PaginatedEventResponse(BaseModel):
    """Paginated event list."""
    items: list[EventResponse]
    total: int
    page: int
    page_size: int
    has_next: bool


# ── Endpoints ───────────────────────────────────────────────────────────────


@router.get(
    "/",
    response_model=PaginatedEventResponse,
    summary="List events",
)
async def list_events(
    city_id: UUID | None = Query(default=None),
    zone_id: UUID | None = Query(default=None),
    category: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """List events with optional filters and pagination."""
    # TODO: Implement events listing service
    return PaginatedEventResponse(items=[], total=0, page=page, page_size=page_size, has_next=False)


@router.post(
    "/",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an event",
)
async def create_event(
    payload: EventCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Create a new event (authentication required)."""
    # TODO: Implement event creation service
    raise NotImplementedError("Event creation not yet implemented.")


@router.get(
    "/{event_id}",
    response_model=EventResponse,
    summary="Get event details",
)
async def get_event(
    event_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get a single event by ID."""
    # TODO: Implement event detail service
    raise NotImplementedError("Event detail not yet implemented.")


@router.get(
    "/upcoming/{city_id}",
    response_model=list[EventResponse],
    summary="Get upcoming events for a city",
)
async def get_upcoming_events(
    city_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get upcoming events for a specific city."""
    # TODO: Implement upcoming events service
    return []
