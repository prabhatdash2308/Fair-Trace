import structlog
from typing import Dict, Any

logger = structlog.get_logger(__name__)

def emit_performance_telemetry(
    execution_id: str,
    workflow_id: str,
    metadata: Dict[str, Any],
    cost_metrics: Dict[str, Any]
) -> None:
    """Emits a structured log event representing a Performance Analysis run."""
    logger.info(
        "performance_agent_execution",
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
        total_tokens=cost_metrics.get("total_tokens")
    )
    
def log_prompt_snapshot(
    execution_id: str, 
    system_prompt: str, 
    developer_prompt: str, 
    prompt_hash: str
) -> None:
    """Records the exact prompts used for absolute reproducibility."""
    logger.debug(
        "prompt_snapshot",
        execution_id=execution_id,
        prompt_hash=prompt_hash,
        system_prompt=system_prompt,
        developer_prompt=developer_prompt
    )
