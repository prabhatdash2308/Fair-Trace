"""FairTrace — Organization ORM Model"""

import uuid
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.db.base import Base, TimestampMixin

class Organization(Base, TimestampMixin):
    __tablename__ = "organizations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    users = relationship("User", back_populates="organization")
    review_cycles = relationship("ReviewCycle", back_populates="organization")
    departments = relationship("Department", back_populates="organization")
    teams = relationship("Team", back_populates="organization")
    goals = relationship("Goal", back_populates="organization")
    feedback = relationship("Feedback", back_populates="organization")
    reviews = relationship("Review", back_populates="organization")
