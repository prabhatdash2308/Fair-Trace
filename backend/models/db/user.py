"""ReviewGuard AI — User ORM Model"""

import uuid
from sqlalchemy import Boolean, Column, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.db.base import Base, TimestampMixin
from models.enums import UserRole


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(Enum(UserRole, name="user_role"), nullable=False)
    manager_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    # Relationships
    manager = relationship("User", remote_side=[id], backref="direct_reports", foreign_keys=[manager_id])
    managed_cycles = relationship(
        "ReviewCycle",
        foreign_keys="ReviewCycle.manager_id",
        back_populates="manager",
    )
    employee_cycles = relationship(
        "ReviewCycle",
        foreign_keys="ReviewCycle.employee_id",
        back_populates="employee",
    )
    submitted_inputs = relationship("ReviewInput", foreign_keys="ReviewInput.submitted_by", back_populates="submitter")
    approved_reports = relationship("Report", foreign_keys="Report.approved_by", back_populates="approver")
