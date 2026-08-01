"""ReviewGuard AI — ReviewInput ORM Model"""

import uuid
from sqlalchemy import Boolean, Column, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import DateTime

from models.db.base import Base, TimestampMixin
from models.enums import InputType


class ReviewInput(Base, TimestampMixin):
    __tablename__ = "review_inputs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    review_cycle_id = Column(
        UUID(as_uuid=True), ForeignKey("review_cycles.id"), nullable=False, index=True
    )
    submitted_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    input_type = Column(Enum(InputType, name="input_type"), nullable=False, index=True)
    content_text = Column(Text, nullable=False)
    is_anonymized = Column(Boolean, nullable=False, default=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    qdrant_document_id = Column(String(255), nullable=True)

    # Relationships
    review_cycle = relationship("ReviewCycle", back_populates="inputs")
    submitter = relationship("User", foreign_keys=[submitted_by], back_populates="submitted_inputs")
    citations = relationship("EvidenceCitation", back_populates="source_input")
    bias_flags = relationship("BiasFlag", back_populates="source_input")
