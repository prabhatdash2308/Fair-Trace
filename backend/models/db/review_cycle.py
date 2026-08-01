"""ReviewGuard AI — ReviewCycle ORM Model"""

import uuid
from sqlalchemy import Column, Date, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.db.base import Base, TimestampMixin
from models.enums import ReviewCycleStatus


class ReviewCycle(Base, TimestampMixin):
    __tablename__ = "review_cycles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    manager_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    review_period_start = Column(Date, nullable=False)
    review_period_end = Column(Date, nullable=False)
    status = Column(
        Enum(ReviewCycleStatus, name="review_cycle_status"),
        nullable=False,
        default=ReviewCycleStatus.DRAFT,
        index=True,
    )

    # Relationships
    employee = relationship("User", foreign_keys=[employee_id], back_populates="employee_cycles")
    manager = relationship("User", foreign_keys=[manager_id], back_populates="managed_cycles")
    creator = relationship("User", foreign_keys=[created_by])
    inputs = relationship("ReviewInput", back_populates="review_cycle", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="review_cycle", cascade="all, delete-orphan")
