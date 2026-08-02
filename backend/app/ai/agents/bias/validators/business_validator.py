from typing import Set
from app.ai.agents.bias.schemas import BiasAnalysisSchema

class BusinessValidator:
    """Applies strict enterprise business rules on the parsed schema."""
    
    @staticmethod
    def validate(analysis: BiasAnalysisSchema) -> None:
        if analysis.overall_bias_score < 0.0 or analysis.overall_bias_score > 1.0:
            raise ValueError("overall_bias_score must be between 0.0 and 1.0.")
            
        if analysis.confidence < 0.0 or analysis.confidence > 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0.")
            
        # Ensure that if biases are detected, the score isn't magically zero
        if analysis.detected_biases and analysis.overall_bias_score == 0.0:
            raise ValueError("overall_bias_score cannot be 0.0 when biases are detected.")
            
        # Verify no duplicate evidence IDs within a single detected bias
        for bias in analysis.detected_biases:
            if len(bias.evidence_ids) != len(set(bias.evidence_ids)):
                raise ValueError(f"Duplicate evidence_ids found in bias: {bias.category}")
