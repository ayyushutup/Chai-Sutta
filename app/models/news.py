"""NewsArticle model – scraped and curated news items."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, text
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.city import City
    from app.models.zone import Zone


class NewsArticle(TimestampMixin, Base):
    """A news article relevant to a city or zone.

    Attributes:
        title: Article headline.
        content: Full article body (optional).
        summary: AI-generated or editorial summary.
        source_url: Original article URL.
        source_name: Publisher / source name.
        category: Topic category (e.g. politics, sports).
        importance_score: AI-assigned importance (0–100).
        zone_id: Optional zone FK for hyper-local articles.
        city_id: Parent city FK.
        location: Optional geo-point for map display.
        ai_metadata: JSONB bag of AI-derived metadata.
        content_hash: SHA-256 hash for deduplication.
        search_vector: PostgreSQL tsvector (GIN indexed).
        status: Publication status (pending / published / rejected).
        published_at: Original publication timestamp.
    """

    __tablename__ = "news_articles"
    __table_args__ = (
        Index("ix_news_city_published", "city_id", "published_at"),
        Index("ix_news_search_vector", "search_vector", postgresql_using="gin"),
    )

    title: Mapped[str] = mapped_column(
        String(500), nullable=False,
    )
    content: Mapped[str | None] = mapped_column(
        Text, nullable=True,
    )
    summary: Mapped[str | None] = mapped_column(
        Text, nullable=True,
    )
    source_url: Mapped[str] = mapped_column(
        String(2000), nullable=False,
    )
    source_name: Mapped[str] = mapped_column(
        String(200), nullable=False,
    )
    category: Mapped[str] = mapped_column(
        String(50), nullable=False,
    )
    importance_score: Mapped[int] = mapped_column(
        Integer, default=0, server_default=text("0"),
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
    ai_metadata: Mapped[dict | None] = mapped_column(
        JSONB, nullable=True,
    )
    content_hash: Mapped[str] = mapped_column(
        String(64), unique=True, index=True, nullable=False,
    )
    search_vector = mapped_column(
        TSVECTOR, nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(20), default="pending", server_default=text("'pending'"), nullable=False,
    )
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True,
    )

    # -- relationships --
    zone: Mapped[Zone | None] = relationship(back_populates="news_articles")
    city: Mapped[City] = relationship()

    def __repr__(self) -> str:
        return f"<NewsArticle title={self.title!r} city_id={self.city_id}>"
