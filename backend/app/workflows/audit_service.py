import structlog
from typing import Dict, Any, Optional

logger = structlog.get_logger(__name__)

class AuditService:
    @staticmethod
    def audit_decision(
        workflow_id: str,
        execution_id: str,
        actor: str,
        decision: str,
        decision_version: str,
        reason: str,
        snapshot: Dict[str, Any]
    ) -> None:
        
        logger.info(
            "workflow_decision_audited",
            workflow_id=workflow_id,
            execution_id=execution_id,
            actor=actor,
            decision=decision,
            decision_version=decision_version,
            reason=reason,
            snapshot_keys=list(snapshot.keys())
        )
