"""Event model – local events, festivals, planned disruptions, etc."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String, Text, text
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.city import City
    from app.models.zone import Zone


class Event(TimestampMixin, Base):
    """A local event (festival, protest, roadwork, etc.).

    Attributes:
        title: Event title / headline.
        description: Detailed description.
        category: Event category (e.g. festival, protest, roadwork).
        zone_id: Optional zone FK.
        city_id: Parent city FK.
        location: Geo-point of the event.
        starts_at: Event start timestamp.
        ends_at: Event end timestamp (optional).
        source: Where the event was sourced from.
        source_url: Link to original listing.
        metadata_: JSONB metadata bag.
        search_vector: PostgreSQL tsvector (GIN indexed).
        is_active: Soft-delete / feature flag.
    """

    __tablename__ = "events"
    __table_args__ = (
        Index("ix_events_search_vector", "search_vector", postgresql_using="gin"),
    )

    title: Mapped[str] = mapped_column(
        String(500), nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True,
    )
    category: Mapped[str] = mapped_column(
        String(50), nullable=False,
    )
    zone_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("zones.id"), nullable=True,
    )
    city_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cities.id"), nullable=False,
    )
    location = mapped_column(
        Geometry("POINT", srid=4326), nullable=True,
    )
    starts_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
    )
    ends_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True,
    )
    source: Mapped[str] = mapped_column(
        String(100), nullable=False,
    )
    source_url: Mapped[str | None] = mapped_column(
        String(2000), nullable=True,
    )
    metadata_: Mapped[dict | None] = mapped_column(
        "metadata", JSONB, nullable=True,
    )
    search_vector = mapped_column(
        TSVECTOR, nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true"),
    )

    # -- relationships --
    zone: Mapped[Zone | None] = relationship(back_populates="events")
    city: Mapped[City] = relationship()

    def __repr__(self) -> str:
        return f"<Event title={self.title!r} starts_at={self.starts_at}>"
