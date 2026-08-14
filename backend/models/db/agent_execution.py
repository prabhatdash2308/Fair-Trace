"""FairTrace — AgentExecution ORM Model"""

import uuid
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from enum import Enum

from models.db.base import Base, TimestampMixin

class AgentStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class AgentSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    NON_CRITICAL = "NON_CRITICAL"

class AgentExecution(Base, TimestampMixin):
    __tablename__ = "agent_executions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_execution_id = Column(String(36), ForeignKey("workflow_executions.id"), nullable=False, index=True)
    
    agent_name = Column(String(100), nullable=False)
    sequence = Column(Integer, nullable=False)
    
    status = Column(SQLEnum(AgentStatus), default=AgentStatus.PENDING, nullable=False)
    severity = Column(SQLEnum(AgentSeverity), default=AgentSeverity.CRITICAL, nullable=False)
    
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    duration_ms = Column(Integer, nullable=True)

    model_provider = Column(String(100), nullable=True)
    model_name = Column(String(100), nullable=True)
    model_version = Column(String(100), nullable=True)
    prompt_version = Column(String(100), nullable=True)

    input_tokens = Column(Integer, nullable=True)
    output_tokens = Column(Integer, nullable=True)
    total_tokens = Column(Integer, nullable=True)

    error_code = Column(String(100), nullable=True)
    error_message = Column(String(2000), nullable=True)

    workflow = relationship("WorkflowExecution", back_populates="agent_executions")
