from typing import Dict, Any, Optional, TypedDict
import datetime

class ExecutionMetadata(TypedDict, total=False):
    execution_id: str
    started_at: str
    updated_at: str
    current_node: str
    previous_node: Optional[str]
    status: str
    retry_count: int
    interrupt_count: int
    checkpoint_count: int

class ReviewState(TypedDict, total=False):
    """
    Strongly typed immutable state for LangGraph.
    Data flows identically through every node.
    """
    # Identifiers
    execution_id: str
    document_id: str
    organization_id: Optional[str]
    user_id: str
    
    # Execution Tracking
    metadata: ExecutionMetadata
    
    # Payloads
    context_bundle: Dict[str, Any]
    
    # Phase 11.7+ AI logic
    performance_analysis: Optional[Dict[str, Any]]
    
    # Phase 11.8 Bias Detection
    bias_analysis: Optional[Dict[str, Any]]
    bias_metrics: Optional[Dict[str, Any]]
    bias_cost: Optional[Dict[str, Any]]
    bias_metadata: Optional[Dict[str, Any]]
    
    # Phase 11.9 Explainability
    explainability_analysis: Optional[Dict[str, Any]]
    explainability_metrics: Optional[Dict[str, Any]]
    explainability_cost: Optional[Dict[str, Any]]
    explainability_metadata: Optional[Dict[str, Any]]
    
    # Phase 11.10 Report Generation
    final_report: Optional[Dict[str, Any]]
    report_metrics: Optional[Dict[str, Any]]
    report_cost: Optional[Dict[str, Any]]
    report_metadata: Optional[Dict[str, Any]]
    
    # Phase 11.11 Human Approval
    approval: Optional[Dict[str, Any]]  # Rich dictionary: status, reviewer_id, comments, decision, requested_revision, approved_at, deadline, revision_count
    
    # Interrupt Logic
    
    # Logging
    telemetry: Dict[str, Any]
