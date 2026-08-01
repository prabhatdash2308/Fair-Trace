"""ReviewGuard AI — ReviewInput ORM Model"""

import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from models.db.base import Base, TimestampMixin
from models.enums import InputType


class ReviewInput(Base, TimestampMixin):
    __tablename__ = "review_inputs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    review_cycle_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("review_cycles.id"), nullable=False, index=True
    )
    submitted_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    input_type: Mapped[InputType] = mapped_column(Enum(InputType, name="input_type"), nullable=False, index=True)
    content_text: Mapped[str] = mapped_column(Text, nullable=False)
    is_anonymized: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    qdrant_document_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relationships
    review_cycle: Mapped["ReviewCycle"] = relationship("ReviewCycle", back_populates="inputs")
    submitter: Mapped["User"] = relationship("User", foreign_keys=[submitted_by], back_populates="submitted_inputs")
    citations: Mapped[List["EvidenceCitation"]] = relationship("EvidenceCitation", back_populates="source_input")
    bias_flags: Mapped[List["BiasFlag"]] = relationship("BiasFlag", back_populates="source_input")
