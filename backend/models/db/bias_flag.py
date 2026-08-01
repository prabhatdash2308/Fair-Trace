"""ReviewGuard AI — BiasFlag ORM Model"""

import uuid
from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from models.db.base import Base, TimestampMixin
from models.enums import BiasType, Severity


class BiasFlag(Base, TimestampMixin):
    __tablename__ = "bias_flags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id = Column(UUID(as_uuid=True), ForeignKey("reports.id"), nullable=False, index=True)
    review_input_id = Column(UUID(as_uuid=True), ForeignKey("review_inputs.id"), nullable=True, index=True)
    bias_type = Column(Enum(BiasType, name="bias_type"), nullable=False, index=True)
    severity = Column(Enum(Severity, name="severity"), nullable=False, index=True)
    affected_text = Column(Text, nullable=True)
    recommended_action = Column(Text, nullable=False)
    detected_by_agent = Column(String(100), nullable=False)
    detection_reasoning = Column(Text, nullable=False)
    detected_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    report = relationship("Report", back_populates="bias_flags")
    source_input = relationship("ReviewInput", back_populates="bias_flags")
