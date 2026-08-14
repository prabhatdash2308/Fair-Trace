"""FairTrace — EvidenceCitation ORM Model"""

import uuid
from typing import Optional
from sqlalchemy import Float, ForeignKey, Integer, Text, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.db.base import Base, TimestampMixin


class EvidenceCitation(Base, TimestampMixin):
    __tablename__ = "evidence_citations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("performance_claims.id"), nullable=True, index=True)
    review_input_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("review_inputs.id"), nullable=False, index=True)
    source_document_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True, index=True)
    source_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    source_reference: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    extracted_passage: Mapped[str] = mapped_column(Text, nullable=False)
    similarity_score: Mapped[float] = mapped_column(Float, nullable=False)
    retrieval_rank: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    claim: Mapped[Optional["PerformanceClaim"]] = relationship("PerformanceClaim", back_populates="citations")
    source_input: Mapped["ReviewInput"] = relationship("ReviewInput", back_populates="citations")
    source_document: Mapped[Optional["Document"]] = relationship("Document")
