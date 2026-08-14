"""FairTrace — Goal ORM Model"""

import uuid
from datetime import date
from typing import List, Optional

from sqlalchemy import Date, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.db.base import Base, TimestampMixin
from models.enums import GoalStatus

class Goal(Base, TimestampMixin):
    __tablename__ = "goals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False, index=True)
    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[GoalStatus] = mapped_column(
        Enum(GoalStatus, name="goal_status"),
        nullable=False,
        default=GoalStatus.NOT_STARTED,
        index=True
    )
    progress: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    due_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    parent_goal_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("goals.id"), nullable=True)

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="goals")
    employee: Mapped["User"] = relationship("User", foreign_keys=[employee_id], back_populates="goals")
    parent_goal: Mapped[Optional["Goal"]] = relationship("Goal", remote_side=[id], backref="child_goals")
