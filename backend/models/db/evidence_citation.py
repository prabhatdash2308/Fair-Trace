"""ReviewGuard AI — EvidenceCitation ORM Model"""

import uuid
from sqlalchemy import Column, Float, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.db.base import Base, TimestampMixin


class EvidenceCitation(Base, TimestampMixin):
    __tablename__ = "evidence_citations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = Column(UUID(as_uuid=True), ForeignKey("performance_claims.id"), nullable=False, index=True)
    review_input_id = Column(UUID(as_uuid=True), ForeignKey("review_inputs.id"), nullable=False, index=True)
    extracted_passage = Column(Text, nullable=False)
    similarity_score = Column(Float, nullable=False)
    retrieval_rank = Column(Integer, nullable=False)

    # Relationships
    claim = relationship("PerformanceClaim", back_populates="citations")
    source_input = relationship("ReviewInput", back_populates="citations")
