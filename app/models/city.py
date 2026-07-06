"""City model – represents a supported city in the platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import Boolean, String, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.zone import Zone


class City(TimestampMixin, Base):
    """A city supported by the Chai Sutta platform.

    Attributes:
        name: Human-readable city name (unique).
        slug: URL-friendly identifier (unique, indexed).
        boundary: Optional polygon boundary of the city.
        metadata_: Flexible JSONB metadata bag.
        is_active: Soft-delete / feature flag.
        zones: Child zones within this city.
    """

    __tablename__ = "cities"

    name: Mapped[str] = mapped_column(
        String(200), unique=True, nullable=False,
    )
    slug: Mapped[str] = mapped_column(
        String(200), unique=True, index=True, nullable=False,
    )
    boundary = mapped_column(
        Geometry("POLYGON", srid=4326), nullable=True,
    )
    metadata_: Mapped[dict | None] = mapped_column(
        "metadata", JSONB, nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true"),
    )

    # -- relationships --
    zones: Mapped[list[Zone]] = relationship(
        back_populates="city", lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<City name={self.name!r} slug={self.slug!r}>"
