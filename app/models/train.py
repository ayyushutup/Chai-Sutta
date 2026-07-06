"""TrainStatus model – real-time local / suburban train statuses."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.city import City
    from app.models.zone import Zone


class TrainStatus(TimestampMixin, Base):
    """Real-time status of a train / local line.

    Attributes:
        train_number: Official train number (if applicable).
        train_name: Human-readable train name.
        line_name: Line / route identifier (e.g. Western, Harbor).
        zone_id: Optional zone FK (nearest zone).
        city_id: City FK.
        status: on_time / delayed / cancelled / diverted.
        delay_minutes: Delay in minutes (0 = on time).
        direction: Direction of travel (e.g. UP, DOWN).
        platform: Platform number / name.
        stations: JSONB list of station stop data.
        source: Data provider.
        recorded_at: When this data was recorded.
    """

    __tablename__ = "train_statuses"

    train_number: Mapped[str | None] = mapped_column(
        String(20), nullable=True,
    )
    train_name: Mapped[str | None] = mapped_column(
        String(200), nullable=True,
    )
    line_name: Mapped[str] = mapped_column(
        String(100), nullable=False,
    )
    zone_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("zones.id"), nullable=True,
    )
    city_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cities.id"), nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20), default="on_time", server_default=text("'on_time'"), nullable=False,
    )
    delay_minutes: Mapped[int] = mapped_column(
        Integer, default=0, server_default=text("0"),
    )
    direction: Mapped[str | None] = mapped_column(
        String(10), nullable=True,
    )
    platform: Mapped[str | None] = mapped_column(
        String(20), nullable=True,
    )
    stations: Mapped[dict | None] = mapped_column(
        JSONB, nullable=True,
    )
    source: Mapped[str] = mapped_column(
        String(100), nullable=False,
    )
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
    )

    # -- relationships --
    zone: Mapped[Zone | None] = relationship()
    city: Mapped[City] = relationship()

    def __repr__(self) -> str:
        return (
            f"<TrainStatus line={self.line_name!r} "
            f"status={self.status!r} delay={self.delay_minutes}m>"
        )
