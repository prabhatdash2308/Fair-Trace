import uuid
import datetime
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, ForeignKey, JSON, Integer, Index, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.db.base import Base
from enum import Enum

class WorkflowStatus(str, Enum):
    RUNNING = "RUNNING"
    WAITING_APPROVAL = "WAITING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REVISION_REQUESTED = "REVISION_REQUESTED"

class ApprovalStatus(str, Enum):
    PENDING = "PENDING"
    IN_REVIEW = "IN_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REVISION_REQUESTED = "REVISION_REQUESTED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"

class WorkflowExecution(Base):
    __tablename__ = "workflow_executions"
    __table_args__ = (
        Index('uq_active_workflow_per_review', 'review_id', unique=True,
              sqlite_where=text("status = 'RUNNING'"), 
              postgresql_where=text("status = 'RUNNING'")),
    )
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    execution_id = Column(String(100), unique=True, nullable=False, index=True)
    graph_thread_id = Column(String(100), nullable=True)
    status = Column(SQLEnum(WorkflowStatus), default=WorkflowStatus.RUNNING, nullable=False)
    current_node = Column(String(100), nullable=True)
    
    started_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    paused_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    last_heartbeat_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    organization_id = Column(String(36), nullable=True)
    review_id = Column(UUID(as_uuid=True), ForeignKey("reviews.id"), nullable=True)
    
    checkpoint_id = Column(String(100), nullable=True)
    current_retry = Column(Integer, default=0)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    metadata_ = Column("metadata", JSON, default=dict)
    
    approvals = relationship("ApprovalRequest", back_populates="workflow", cascade="all, delete-orphan")
    history = relationship("WorkflowHistory", back_populates="workflow", cascade="all, delete-orphan")
    agent_executions = relationship("AgentExecution", back_populates="workflow", cascade="all, delete-orphan")

class ApprovalRequest(Base):
    __tablename__ = "approval_requests"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_id = Column(String(36), ForeignKey("workflow_executions.id"), nullable=False)
    execution_id = Column(String(100), nullable=False)
    report_id = Column(String(100), nullable=True)
    reviewer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    status = Column(SQLEnum(ApprovalStatus), default=ApprovalStatus.PENDING, nullable=False)
    decision = Column(String(50), nullable=True)
    decision_version = Column(String(50), nullable=True)
    decision_reason = Column(String(2000), nullable=True)
    decision_timestamp = Column(DateTime(timezone=True), nullable=True)
    reviewer_snapshot = Column(JSON, default=dict)
    
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    deadline = Column(DateTime(timezone=True), nullable=True)
    revision_count = Column(Integer, default=0)
    metadata_ = Column("metadata", JSON, default=dict)
    
    workflow = relationship("WorkflowExecution", back_populates="approvals")

class WorkflowHistory(Base):
    __tablename__ = "workflow_history"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_id = Column(String(36), ForeignKey("workflow_executions.id"), nullable=False)
    event = Column(String(100), nullable=False)
    trigger = Column(String(100), nullable=False)
    node = Column(String(100), nullable=True)
    
    previous_status = Column(String(50), nullable=True)
    new_status = Column(String(50), nullable=True)
    
    actor = Column(String(100), nullable=True)
    timestamp = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    
    duration_ms = Column(Integer, nullable=True)
    execution_id = Column(String(100), nullable=True)
    checkpoint_id = Column(String(100), nullable=True)
    details = Column(JSON, default=dict)
    
    workflow = relationship("WorkflowExecution", back_populates="history")
