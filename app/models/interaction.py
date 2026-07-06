"""UserInteraction model – tracks user actions (upvote, bookmark, share, etc.)."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class UserInteraction(TimestampMixin, Base):
    """A record of a user's interaction with a content entity.

    Attributes:
        user_id: User FK.
        entity_type: Type of the target entity (e.g. news, report, event).
        entity_id: UUID of the target entity (polymorphic reference).
        action: Interaction type (upvote, downvote, bookmark, share, view).
    """

    __tablename__ = "user_interactions"
    __table_args__ = (
        Index(
            "ix_interactions_user_entity",
            "user_id",
            "entity_type",
            "entity_id",
        ),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False,
    )
    entity_type: Mapped[str] = mapped_column(
        String(20), nullable=False,
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False,
    )
    action: Mapped[str] = mapped_column(
        String(20), nullable=False,
    )

    # -- relationships --
    user: Mapped[User] = relationship(back_populates="interactions")

    def __repr__(self) -> str:
        return (
            f"<UserInteraction user_id={self.user_id} "
            f"action={self.action!r} entity_type={self.entity_type!r}>"
        )
