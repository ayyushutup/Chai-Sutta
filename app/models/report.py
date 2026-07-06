"""CommunityReport model – user-submitted reports (incidents, tips, etc.)."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text, text
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.city import City
    from app.models.user import User
    from app.models.zone import Zone


class CommunityReport(TimestampMixin, Base):
    """A community-submitted report (pothole, incident, tip, etc.).

    Attributes:
        user_id: Author FK.
        zone_id: Optional zone FK.
        city_id: Parent city FK.
        location: Geo-point where the report applies.
        category: Report category (e.g. pothole, crime).
        severity: Severity level (low / medium / high / critical).
        content: User-provided description.
        ai_extracted_text: Text extracted by AI from media.
        ai_metadata: JSONB AI analysis metadata.
        media_type: Type of attached media (none / image / video).
        media_url: URL to attached media.
        upvotes: Community upvote count.
        downvotes: Community downvote count.
        verification_status: Moderation status (unverified / verified / rejected).
        search_vector: PostgreSQL tsvector (GIN indexed).
        expires_at: Optional expiry timestamp.
        is_active: Soft-delete / feature flag.
    """

    __tablename__ = "community_reports"
    __table_args__ = (
        Index(
            "ix_reports_search_vector",
            "search_vector",
            postgresql_using="gin",
        ),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False,
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
    category: Mapped[str] = mapped_column(
        String(50), nullable=False,
    )
    severity: Mapped[str] = mapped_column(
        String(20), default="low", server_default=text("'low'"), nullable=False,
    )
    content: Mapped[str] = mapped_column(
        Text, nullable=False,
    )
    ai_extracted_text: Mapped[str | None] = mapped_column(
        Text, nullable=True,
    )
    ai_metadata: Mapped[dict | None] = mapped_column(
        JSONB, nullable=True,
    )
    media_type: Mapped[str] = mapped_column(
        String(20), default="none", server_default=text("'none'"), nullable=False,
    )
    media_url: Mapped[str | None] = mapped_column(
        String(2000), nullable=True,
    )
    upvotes: Mapped[int] = mapped_column(
        Integer, default=0, server_default=text("0"),
    )
    downvotes: Mapped[int] = mapped_column(
        Integer, default=0, server_default=text("0"),
    )
    verification_status: Mapped[str] = mapped_column(
        String(20),
        default="unverified",
        server_default=text("'unverified'"),
        nullable=False,
    )
    search_vector = mapped_column(
        TSVECTOR, nullable=True,
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true"),
    )

    # -- relationships --
    user: Mapped[User] = relationship(back_populates="reports")
    zone: Mapped[Zone | None] = relationship(back_populates="reports")
    city: Mapped[City] = relationship()

    def __repr__(self) -> str:
        return f"<CommunityReport category={self.category!r} user_id={self.user_id}>"
