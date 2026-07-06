"""User model – platform users with auth and profile data."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.interaction import UserInteraction
    from app.models.report import CommunityReport
    from app.models.zone import Zone


class User(TimestampMixin, Base):
    """A registered user of the Chai Sutta platform.

    Attributes:
        email: Unique email address (indexed).
        phone: Optional phone number.
        display_name: Public display name.
        avatar_url: Profile picture URL.
        auth_provider: OAuth provider or 'email'.
        auth_provider_id: External provider user ID.
        password_hash: Hashed password (email auth only).
        home_zone_id: User's preferred home zone FK.
        preferences: JSONB user preferences.
        reputation_score: Community reputation points.
        is_active: Soft-delete / feature flag.
    """

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(320), unique=True, index=True, nullable=False,
    )
    phone: Mapped[str | None] = mapped_column(
        String(20), nullable=True,
    )
    display_name: Mapped[str] = mapped_column(
        String(100), nullable=False,
    )
    avatar_url: Mapped[str | None] = mapped_column(
        String(2000), nullable=True,
    )
    auth_provider: Mapped[str] = mapped_column(
        String(20), nullable=False, default="email",
    )
    auth_provider_id: Mapped[str | None] = mapped_column(
        String(500), nullable=True,
    )
    password_hash: Mapped[str | None] = mapped_column(
        String(500), nullable=True,
    )
    home_zone_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("zones.id"), nullable=True,
    )
    preferences: Mapped[dict] = mapped_column(
        JSONB, default=dict, server_default=text("'{}'"),
    )
    reputation_score: Mapped[int] = mapped_column(
        Integer, default=0, server_default=text("0"),
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true"),
    )

    # -- relationships --
    reports: Mapped[list[CommunityReport]] = relationship(back_populates="user")
    interactions: Mapped[list[UserInteraction]] = relationship(back_populates="user")
    home_zone: Mapped[Zone | None] = relationship()

    def __repr__(self) -> str:
        return f"<User email={self.email!r} display_name={self.display_name!r}>"
