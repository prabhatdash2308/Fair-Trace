"""FairTrace — Feedback ORM Model"""

import uuid
from typing import List, Optional

from sqlalchemy import Boolean, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.db.base import Base, TimestampMixin
from models.enums import FeedbackType

class Feedback(Base, TimestampMixin):
    __tablename__ = "feedback"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False, index=True)
    author_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    recipient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    review_cycle_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("review_cycles.id"), nullable=True, index=True)
    feedback_type: Mapped[FeedbackType] = mapped_column(
        Enum(FeedbackType, name="feedback_type"),
        nullable=False,
        default=FeedbackType.GENERAL
    )
    project: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    content_text: Mapped[str] = mapped_column(Text, nullable=False)
    tags: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_requested: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="feedback")
    author: Mapped["User"] = relationship("User", foreign_keys=[author_id], back_populates="feedback_given")
    recipient: Mapped["User"] = relationship("User", foreign_keys=[recipient_id], back_populates="feedback_received")
    review_cycle: Mapped[Optional["ReviewCycle"]] = relationship("ReviewCycle")
