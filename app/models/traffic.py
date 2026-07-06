"""TrafficData model – real-time traffic snapshots per zone / road segment."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import DateTime, Float, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.city import City
    from app.models.zone import Zone


class TrafficData(TimestampMixin, Base):
    """A traffic data snapshot for a zone or road segment.

    Attributes:
        zone_id: Zone FK.
        city_id: City FK.
        location: Geo-point for the measurement.
        road_name: Name of the road / segment.
        current_speed: Observed speed (km/h).
        free_flow_speed: Expected free-flow speed (km/h).
        congestion_level: free_flow / light / moderate / heavy / standstill.
        incidents: JSONB list of incidents on this segment.
        source: Data provider (e.g. tomtom, google).
        recorded_at: When this data was recorded.
    """

    __tablename__ = "traffic_data"

    zone_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("zones.id"), nullable=False,
    )
    city_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cities.id"), nullable=False,
    )
    location = mapped_column(
        Geometry("POINT", srid=4326), nullable=True,
    )
    road_name: Mapped[str | None] = mapped_column(
        String(300), nullable=True,
    )
    current_speed: Mapped[float] = mapped_column(
        Float, nullable=False,
    )
    free_flow_speed: Mapped[float] = mapped_column(
        Float, nullable=False,
    )
    congestion_level: Mapped[str] = mapped_column(
        String(20),
        default="free_flow",
        server_default=text("'free_flow'"),
        nullable=False,
    )
    incidents: Mapped[dict | None] = mapped_column(
        JSONB, nullable=True,
    )
    source: Mapped[str] = mapped_column(
        String(100), default="tomtom", server_default=text("'tomtom'"), nullable=False,
    )
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
    )

    # -- relationships --
    zone: Mapped[Zone] = relationship()
    city: Mapped[City] = relationship()

    def __repr__(self) -> str:
        return (
            f"<TrafficData zone_id={self.zone_id} "
            f"congestion={self.congestion_level!r}>"
        )
