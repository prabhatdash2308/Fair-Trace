"""ReviewGuard AI — Report ORM Model"""

import uuid
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from models.db.base import Base, TimestampMixin
from models.enums import ReportStatus, ConfidenceLevel


class Report(Base, TimestampMixin):
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    review_cycle_id = Column(
        UUID(as_uuid=True), ForeignKey("review_cycles.id"), nullable=False, index=True
    )
    version = Column(Integer, nullable=False, default=1)
    status = Column(
        Enum(ReportStatus, name="report_status"),
        nullable=False,
        default=ReportStatus.DRAFT,
        index=True,
    )
    executive_summary = Column(Text, nullable=True)
    recommended_actions = Column(JSONB, nullable=True)  # List[str]
    confidence_score = Column(Enum(ConfidenceLevel, name="confidence_level"), nullable=True)
    confidence_explanation = Column(Text, nullable=True)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    approval_reason = Column(Text, nullable=True)
    pipeline_run_id = Column(String(255), nullable=False, index=True)
    is_current = Column(Boolean, nullable=False, default=True, index=True)
    generated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    approval_idempotency_key = Column(String(255), nullable=True, unique=True)

    # Relationships
    review_cycle = relationship("ReviewCycle", back_populates="reports")
    approver = relationship("User", foreign_keys=[approved_by], back_populates="approved_reports")
    claims = relationship(
        "PerformanceClaim", back_populates="report", cascade="all, delete-orphan"
    )
    bias_flags = relationship("BiasFlag", back_populates="report", cascade="all, delete-orphan")
