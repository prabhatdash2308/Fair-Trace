from app.ai.agents.explainability.schemas import ExplainabilityAnalysisSchema

class BusinessValidator:
    """Applies strict enterprise business rules for explainability."""
    
    @staticmethod
    def validate(analysis: ExplainabilityAnalysisSchema) -> None:
        if analysis.overall_confidence < 0.0 or analysis.overall_confidence > 1.0:
            raise ValueError("overall_confidence must be between 0.0 and 1.0.")
            
        # Every reasoning trace must have at least one evidence ID (no hallucination)
        for trace in analysis.reasoning_trace:
            if not trace.evidence_ids:
                raise ValueError(f"Reasoning trace '{trace.finding}' is missing evidence IDs.")
                
            # No duplicate chunk references
            if len(trace.evidence_ids) != len(set(trace.evidence_ids)):
                raise ValueError(f"Reasoning trace '{trace.finding}' contains duplicate evidence IDs.")
                
        # If there are unsupported claims, ensure reasoning exists for them
        # (Already somewhat enforced by Pydantic, but can add custom checks if needed)
