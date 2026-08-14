"""FairTrace — BiasFlag ORM Model"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from models.db.base import Base, TimestampMixin
from models.enums import BiasType, Severity


class BiasFlag(Base, TimestampMixin):
    __tablename__ = "bias_flags"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("reports.id"), nullable=False, index=True)
    review_input_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("review_inputs.id"), nullable=True, index=True)
    bias_type: Mapped[BiasType] = mapped_column(Enum(BiasType, name="bias_type"), nullable=False, index=True)
    severity: Mapped[Severity] = mapped_column(Enum(Severity, name="severity"), nullable=False, index=True)
    affected_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recommended_action: Mapped[str] = mapped_column(Text, nullable=False)
    detected_by_agent: Mapped[str] = mapped_column(String(100), nullable=False)
    detection_reasoning: Mapped[str] = mapped_column(Text, nullable=False)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    report: Mapped["Report"] = relationship("Report", back_populates="bias_flags")
    source_input: Mapped[Optional["ReviewInput"]] = relationship("ReviewInput", back_populates="bias_flags")
