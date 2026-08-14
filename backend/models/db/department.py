"""FairTrace — Department ORM Model"""

import uuid
from typing import List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.db.base import Base, TimestampMixin

class Department(Base, TimestampMixin):
    __tablename__ = "departments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    head_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="departments")
    head: Mapped[Optional["User"]] = relationship("User", foreign_keys=[head_id])
    teams: Mapped[List["Team"]] = relationship("Team", back_populates="department")
    users: Mapped[List["User"]] = relationship("User", back_populates="department", foreign_keys="User.department_id")
