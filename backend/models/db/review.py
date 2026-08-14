"""FairTrace — Review ORM Model"""

import uuid
from datetime import date
from typing import List, Optional

from sqlalchemy import Date, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.db.base import Base, TimestampMixin
from models.enums import ReviewStatus


class Review(Base, TimestampMixin):
    __tablename__ = "reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    review_cycle_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("review_cycles.id"), nullable=False, index=True)
    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    manager_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    review_period_start: Mapped[date] = mapped_column(Date, nullable=False)
    review_period_end: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[ReviewStatus] = mapped_column(
        Enum(ReviewStatus, name="review_status"),
        nullable=False,
        default=ReviewStatus.DRAFT,
        index=True,
    )

    # Relationships
    review_cycle: Mapped["ReviewCycle"] = relationship("ReviewCycle", back_populates="reviews")
    employee: Mapped["User"] = relationship("User", foreign_keys=[employee_id], back_populates="employee_reviews")
    manager: Mapped["User"] = relationship("User", foreign_keys=[manager_id], back_populates="managed_reviews")
    creator: Mapped["User"] = relationship("User", foreign_keys=[created_by])
    organization: Mapped[Optional["Organization"]] = relationship("Organization", back_populates="reviews")
    inputs: Mapped[List["ReviewInput"]] = relationship("ReviewInput", back_populates="review", cascade="all, delete-orphan")
    reports: Mapped[List["Report"]] = relationship("Report", back_populates="review", cascade="all, delete-orphan")
