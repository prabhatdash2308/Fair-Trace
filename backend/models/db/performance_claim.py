"""FairTrace — PerformanceClaim ORM Model"""

import uuid
from typing import List

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.db.base import Base, TimestampMixin
from models.enums import PerformanceDimension, ConfidenceLevel


class PerformanceClaim(Base, TimestampMixin):
    __tablename__ = "performance_claims"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("reports.id"), nullable=False, index=True)
    dimension: Mapped[PerformanceDimension] = mapped_column(Enum(PerformanceDimension, name="performance_dimension"), nullable=False, index=True)
    claim_text: Mapped[str] = mapped_column(Text, nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False, default="")
    confidence: Mapped[ConfidenceLevel] = mapped_column(Enum(ConfidenceLevel, name="confidence_level"), nullable=False)
    is_supported: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Relationships
    report: Mapped["Report"] = relationship("Report", back_populates="claims")
    citations: Mapped[List["EvidenceCitation"]] = relationship(
        "EvidenceCitation", back_populates="claim", cascade="all, delete-orphan"
    )
