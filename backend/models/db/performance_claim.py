"""ReviewGuard AI — PerformanceClaim ORM Model"""

import uuid
from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.db.base import Base, TimestampMixin
from models.enums import PerformanceDimension, ConfidenceLevel


class PerformanceClaim(Base, TimestampMixin):
    __tablename__ = "performance_claims"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id = Column(UUID(as_uuid=True), ForeignKey("reports.id"), nullable=False, index=True)
    dimension = Column(Enum(PerformanceDimension, name="performance_dimension"), nullable=False, index=True)
    claim_text = Column(Text, nullable=False)
    explanation = Column(Text, nullable=False, default="")
    confidence = Column(Enum(ConfidenceLevel, name="confidence_level"), nullable=False)
    is_supported = Column(Boolean, nullable=False, default=True)
    display_order = Column(Integer, nullable=False, default=0)

    # Relationships
    report = relationship("Report", back_populates="claims")
    citations = relationship(
        "EvidenceCitation", back_populates="claim", cascade="all, delete-orphan"
    )
