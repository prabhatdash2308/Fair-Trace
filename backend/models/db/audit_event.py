"""ReviewGuard AI — AuditEvent ORM Model (write-once, immutable)"""

import uuid
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from models.db.base import Base
from models.enums import AuditEventType, UserRole


class AuditEvent(Base):
    """
    Immutable audit log entry.
    No TimestampMixin — only occurred_at, no updated_at.
    No update or delete operations permitted at any layer.
    """

    __tablename__ = "audit_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(Enum(AuditEventType, name="audit_event_type"), nullable=False, index=True)
    actor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    actor_role = Column(Enum(UserRole, name="user_role"), nullable=True)
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    event_payload = Column(JSONB, nullable=False)
    occurred_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    ip_address = Column(String(45), nullable=True)
    correlation_id = Column(String(255), nullable=True, index=True)
    state_version = Column(Integer, nullable=True)
    prompt_version = Column(String(50), nullable=True)

    actor = relationship("User", foreign_keys=[actor_id])
