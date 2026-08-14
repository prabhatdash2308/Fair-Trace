"""FairTrace — Team ORM Model"""

import uuid
from typing import List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.db.base import Base, TimestampMixin

class Team(Base, TimestampMixin):
    __tablename__ = "teams"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False, index=True)
    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    lead_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="teams")
    department: Mapped[Optional["Department"]] = relationship("Department", back_populates="teams")
    lead: Mapped[Optional["User"]] = relationship("User", foreign_keys=[lead_id])
    users: Mapped[List["User"]] = relationship("User", back_populates="team", foreign_keys="User.team_id")
