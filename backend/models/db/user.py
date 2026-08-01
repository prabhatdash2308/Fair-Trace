"""ReviewGuard AI — User ORM Model"""

import uuid
from typing import List, Optional

from sqlalchemy import Boolean, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.db.base import Base, TimestampMixin
from models.enums import UserRole


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"), nullable=False)
    manager_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Relationships
    manager: Mapped[Optional["User"]] = relationship("User", remote_side=[id], backref="direct_reports", foreign_keys=[manager_id])
    managed_cycles: Mapped[List["ReviewCycle"]] = relationship(
        "ReviewCycle",
        foreign_keys="ReviewCycle.manager_id",
        back_populates="manager",
    )
    employee_cycles: Mapped[List["ReviewCycle"]] = relationship(
        "ReviewCycle",
        foreign_keys="ReviewCycle.employee_id",
        back_populates="employee",
    )
    submitted_inputs: Mapped[List["ReviewInput"]] = relationship("ReviewInput", foreign_keys="ReviewInput.submitted_by", back_populates="submitter")
    approved_reports: Mapped[List["Report"]] = relationship("Report", foreign_keys="Report.approved_by", back_populates="approver")
