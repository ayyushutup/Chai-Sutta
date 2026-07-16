"""Events routes: list, create, detail, and upcoming."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.core.geo import point_from_coords
from app.models.event import Event
from app.models.user import User
from app.schemas.common import PaginatedResponse
from app.schemas.event import EventCreate, EventResponse

router = APIRouter()


# ── Endpoints ───────────────────────────────────────────────────────────────


@router.get(
    "/",
    response_model=PaginatedResponse[EventResponse],
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
    stmt = select(Event).where(Event.is_active == True)

    if city_id:
        stmt = stmt.where(Event.city_id == city_id)
    if zone_id:
        stmt = stmt.where(Event.zone_id == zone_id)
    if category:
        stmt = stmt.where(Event.category == category)

    stmt = stmt.order_by(Event.starts_at.asc())

    # Total count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar_one()

    # Paginate
    stmt = stmt.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(stmt)
    events = result.scalars().all()

    return PaginatedResponse(
        items=[EventResponse.model_validate(e) for e in events],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post(
    "/",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an event",
)
async def create_event(
    payload: EventCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Create a new event (authentication required)."""
    location = None
    if payload.location:
        location = point_from_coords(payload.location.lat, payload.location.lon)

    event = Event(
        title=payload.title,
        description=payload.description,
        category=payload.category,
        city_id=payload.city_id,
        zone_id=payload.zone_id,
        location=location,
        starts_at=payload.starts_at,
        ends_at=payload.ends_at,
        source="user",
        is_active=True,
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return EventResponse.model_validate(event)


@router.get(
    "/upcoming/{city_id}",
    response_model=list[EventResponse],
    summary="Get upcoming events for a city",
)
async def get_upcoming_events(
    city_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get upcoming events for a specific city, sorted by start time."""
    now = datetime.now(timezone.utc)
    stmt = (
        select(Event)
        .where(Event.city_id == city_id, Event.is_active == True, Event.starts_at >= now)
        .order_by(Event.starts_at.asc())
        .limit(20)
    )
    result = await db.execute(stmt)
    events = result.scalars().all()
    return [EventResponse.model_validate(e) for e in events]


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
    result = await db.execute(
        select(Event).where(Event.id == event_id, Event.is_active == True)
    )
    event = result.scalar_one_or_none()
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found.")
    return EventResponse.model_validate(event)
