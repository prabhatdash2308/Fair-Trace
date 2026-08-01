"""ReviewGuard AI — ReviewCycle ORM Model"""

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
    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    manager_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    review_period_start: Mapped[date] = mapped_column(Date, nullable=False)
    review_period_end: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[ReviewCycleStatus] = mapped_column(
        Enum(ReviewCycleStatus, name="review_cycle_status"),
        nullable=False,
        default=ReviewCycleStatus.DRAFT,
        index=True,
    )

    # Relationships
    employee: Mapped["User"] = relationship("User", foreign_keys=[employee_id], back_populates="employee_cycles")
    manager: Mapped["User"] = relationship("User", foreign_keys=[manager_id], back_populates="managed_cycles")
    creator: Mapped["User"] = relationship("User", foreign_keys=[created_by])
    inputs: Mapped[List["ReviewInput"]] = relationship("ReviewInput", back_populates="review_cycle", cascade="all, delete-orphan")
    reports: Mapped[List["Report"]] = relationship("Report", back_populates="review_cycle", cascade="all, delete-orphan")
