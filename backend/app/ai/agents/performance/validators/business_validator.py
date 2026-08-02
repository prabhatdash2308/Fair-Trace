from typing import Set
from app.ai.agents.performance.schemas import PerformanceAnalysisSchema
from app.ai.agents.performance.exceptions import OutputValidationError

class BusinessValidator:
    """Applies strict enterprise business rules on the parsed schema."""
    
    @staticmethod
    def validate(analysis: PerformanceAnalysisSchema) -> None:
        if analysis.overall_score < 1 or analysis.overall_score > 5:
            raise OutputValidationError("overall_score must be between 1 and 5.")
            
        if analysis.confidence < 0.0 or analysis.confidence > 1.0:
            raise OutputValidationError("confidence must be between 0.0 and 1.0.")
            
        if not analysis.key_observations:
            raise OutputValidationError("Analysis must contain at least one key observation.")
            
        if not analysis.analysis_summary or len(analysis.analysis_summary.strip()) < 50:
            raise OutputValidationError("Analysis summary must be at least 50 characters long.")
            
        # Check for duplicate evidence strings
        evidence_set: Set[str] = set()
        for obs in analysis.key_observations:
            ev = obs.evidence.strip().lower()
            if not ev:
                raise OutputValidationError("Observations must have non-empty evidence.")
            if ev in evidence_set:
                # We can either raise or just log. Strict mode: raise
                raise OutputValidationError(f"Duplicate evidence found: '{obs.evidence}'")
            evidence_set.add(ev)
