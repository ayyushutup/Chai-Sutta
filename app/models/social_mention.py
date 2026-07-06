"""SocialMention model – social media posts mentioning a city / zone."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.city import City
    from app.models.zone import Zone


class SocialMention(TimestampMixin, Base):
    """A social media mention related to a city or zone.

    Attributes:
        platform: Social platform (twitter, reddit, instagram, etc.).
        post_id: Platform-specific post identifier.
        content: Post text content.
        author: Author handle / display name.
        engagement_score: Combined engagement metric.
        zone_id: Optional zone FK.
        city_id: City FK.
        category: Topic category (optional).
        ai_metadata: JSONB AI analysis results.
        search_vector: PostgreSQL tsvector (GIN indexed).
        posted_at: Original post timestamp.
    """

    __tablename__ = "social_mentions"
    __table_args__ = (
        UniqueConstraint("platform", "post_id", name="uq_social_mention_platform_post"),
        Index(
            "ix_social_mentions_search_vector",
            "search_vector",
            postgresql_using="gin",
        ),
    )

    platform: Mapped[str] = mapped_column(
        String(50), nullable=False,
    )
    post_id: Mapped[str | None] = mapped_column(
        String(500), nullable=True,
    )
    content: Mapped[str] = mapped_column(
        Text, nullable=False,
    )
    author: Mapped[str | None] = mapped_column(
        String(200), nullable=True,
    )
    engagement_score: Mapped[int] = mapped_column(
        Integer, default=0, server_default=text("0"),
    )
    zone_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("zones.id"), nullable=True,
    )
    city_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cities.id"), nullable=False,
    )
    category: Mapped[str | None] = mapped_column(
        String(50), nullable=True,
    )
    ai_metadata: Mapped[dict | None] = mapped_column(
        JSONB, nullable=True,
    )
    search_vector = mapped_column(
        TSVECTOR, nullable=True,
    )
    posted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
    )

    # -- relationships --
    zone: Mapped[Zone | None] = relationship()
    city: Mapped[City] = relationship()

    def __repr__(self) -> str:
        return (
            f"<SocialMention platform={self.platform!r} "
            f"post_id={self.post_id!r}>"
        )
