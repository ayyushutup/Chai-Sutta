"""Zone model – a sub-region within a city (neighborhood, ward, etc.)."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import Boolean, ForeignKey, Index, String, text
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.city import City
    from app.models.event import Event
    from app.models.news import NewsArticle
    from app.models.report import CommunityReport


class Zone(TimestampMixin, Base):
    """A zone (neighborhood / ward) within a city.

    Attributes:
        city_id: Parent city FK.
        name: Human-readable zone name.
        slug: URL-friendly identifier (indexed).
        boundary: Optional polygon boundary.
        centroid: Representative center point.
        zone_type: Classification (e.g. neighborhood, ward).
        search_vector: PostgreSQL tsvector for full-text search (GIN indexed).
        is_active: Soft-delete / feature flag.
    """

    __tablename__ = "zones"
    __table_args__ = (
        Index("ix_zones_search_vector", "search_vector", postgresql_using="gin"),
    )

    city_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cities.id"), nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(200), nullable=False,
    )
    slug: Mapped[str] = mapped_column(
        String(200), index=True, nullable=False,
    )
    boundary = mapped_column(
        Geometry("POLYGON", srid=4326), nullable=True,
    )
    centroid = mapped_column(
        Geometry("POINT", srid=4326), nullable=True,
    )
    zone_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="neighborhood",
    )
    search_vector = mapped_column(
        TSVECTOR, nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true"),
    )

    # -- relationships --
    city: Mapped[City] = relationship(back_populates="zones")
    news_articles: Mapped[list[NewsArticle]] = relationship(back_populates="zone")
    reports: Mapped[list[CommunityReport]] = relationship(back_populates="zone")
    events: Mapped[list[Event]] = relationship(back_populates="zone")

    def __repr__(self) -> str:
        return f"<Zone name={self.name!r} city_id={self.city_id}>"
