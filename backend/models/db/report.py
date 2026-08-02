"""ReviewGuard AI — Report ORM Model"""

import uuid
from datetime import datetime
from typing import Any, List, Optional

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from models.db.base import Base, TimestampMixin
from models.enums import ReportStatus, ConfidenceLevel


class Report(Base, TimestampMixin):
    __tablename__ = "reports"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    review_cycle_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("review_cycles.id"), nullable=False, index=True
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[ReportStatus] = mapped_column(
        Enum(ReportStatus, name="report_status"),
        nullable=False,
        default=ReportStatus.DRAFT,
        index=True,
    )
    executive_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recommended_actions: Mapped[Optional[List[str]]] = mapped_column(JSON().with_variant(JSONB, "postgresql"), nullable=True)  # List[str]
    confidence_score: Mapped[Optional[ConfidenceLevel]] = mapped_column(Enum(ConfidenceLevel, name="confidence_level"), nullable=True)
    confidence_explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    approved_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    approval_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    pipeline_run_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    is_current: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    approval_idempotency_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, unique=True)

    # Relationships
    review_cycle: Mapped["ReviewCycle"] = relationship("ReviewCycle", back_populates="reports")
    approver: Mapped[Optional["User"]] = relationship("User", foreign_keys=[approved_by], back_populates="approved_reports")
    claims: Mapped[List["PerformanceClaim"]] = relationship(
        "PerformanceClaim", back_populates="report", cascade="all, delete-orphan"
    )
    bias_flags: Mapped[List["BiasFlag"]] = relationship("BiasFlag", back_populates="report", cascade="all, delete-orphan")
