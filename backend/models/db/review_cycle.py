"""FairTrace — ReviewCycle ORM Model (Organization-wide Process)"""

import uuid
from datetime import date
from typing import List

from sqlalchemy import Date, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.db.base import Base, TimestampMixin
from models.enums import ReviewCycleStatus


class ReviewCycle(Base, TimestampMixin):
    __tablename__ = "review_cycles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False, index=True)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[ReviewCycleStatus] = mapped_column(
        Enum(ReviewCycleStatus, name="review_cycle_status"),
        nullable=False,
        default=ReviewCycleStatus.DRAFT,
        index=True,
    )

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="review_cycles")
    creator: Mapped["User"] = relationship("User", foreign_keys=[created_by])
    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="review_cycle", cascade="all, delete-orphan")
