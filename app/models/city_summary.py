"""CitySummary model – AI-generated periodic city / zone summaries."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.city import City
    from app.models.zone import Zone


class CitySummary(TimestampMixin, Base):
    """AI-generated summary of a city's current state.

    Attributes:
        city_id: City FK.
        zone_id: Optional zone FK (zone-level summary).
        summary_text: The generated summary.
        mood: Overall mood label (e.g. calm, tense, festive).
        mood_score: Numeric mood score (0–100).
        mood_emoji: Emoji representation of the mood.
        data_snapshot: JSONB snapshot of source data used.
        trending_topics: JSONB list of trending topics.
        generated_at: When this summary was generated.
    """

    __tablename__ = "city_summaries"
    __table_args__ = (
        Index("ix_city_summaries_city_generated", "city_id", "generated_at"),
    )

    city_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cities.id"), nullable=False,
    )
    zone_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("zones.id"), nullable=True,
    )
    summary_text: Mapped[str] = mapped_column(
        Text, nullable=False,
    )
    mood: Mapped[str] = mapped_column(
        String(20), nullable=False,
    )
    mood_score: Mapped[int] = mapped_column(
        Integer, nullable=False,
    )
    mood_emoji: Mapped[str] = mapped_column(
        String(10), nullable=False,
    )
    data_snapshot: Mapped[dict | None] = mapped_column(
        JSONB, nullable=True,
    )
    trending_topics: Mapped[dict | None] = mapped_column(
        JSONB, nullable=True,
    )
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
    )

    # -- relationships --
    city: Mapped[City] = relationship()
    zone: Mapped[Zone | None] = relationship()

    def __repr__(self) -> str:
        return (
            f"<CitySummary city_id={self.city_id} "
            f"mood={self.mood!r} generated_at={self.generated_at}>"
        )
