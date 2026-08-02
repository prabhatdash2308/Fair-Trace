import structlog
from typing import Dict, Any

logger = structlog.get_logger(__name__)

def emit_report_telemetry(
    execution_id: str,
    workflow_id: str,
    metadata: Dict[str, Any],
    cost_metrics: Dict[str, Any],
    report_length: int,
    recommendation_count: int,
    strength_count: int,
    improvement_count: int,
    risk_count: int,
    evidence_count: int,
    overall_score: float,
    confidence: float
) -> None:
    logger.info(
        "report_generation_agent_execution",
        execution_id=execution_id,
        workflow_id=workflow_id,
        agent_version=metadata.get("agent_version"),
        prompt_version=metadata.get("prompt_version"),
        prompt_hash=metadata.get("prompt_hash"),
        model=metadata.get("model"),
        provider=metadata.get("provider"),
        latency_s=metadata.get("latency_s"),
        retries=metadata.get("retries"),
        total_cost=cost_metrics.get("total_cost"),
        total_tokens=cost_metrics.get("total_tokens"),
        report_length=report_length,
        recommendation_count=recommendation_count,
        strength_count=strength_count,
        improvement_count=improvement_count,
        risk_count=risk_count,
        evidence_count=evidence_count,
        overall_score=overall_score,
        confidence=confidence
    )
    
def log_prompt_snapshot(
    execution_id: str, 
    system_prompt: str, 
    developer_prompt: str, 
    prompt_hash: str
) -> None:
    logger.debug(
        "prompt_snapshot_report",
        execution_id=execution_id,
        prompt_hash=prompt_hash,
        system_prompt=system_prompt,
        developer_prompt=developer_prompt
    )
