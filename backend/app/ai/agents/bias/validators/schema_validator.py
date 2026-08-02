from typing import Any, Dict
from pydantic import ValidationError
from app.ai.agents.bias.schemas import BiasAnalysisSchema

class SchemaValidator:
    """Validates raw output dictionaries against the strict Pydantic Bias schema."""
    
    @staticmethod
    def validate(raw_data: Dict[str, Any]) -> BiasAnalysisSchema:
        try:
            return BiasAnalysisSchema.model_validate(raw_data)
        except ValidationError as e:
            # We raise a standard ValueError here, which will be caught and wrapped by the agent
            raise ValueError(f"Schema validation failed: {str(e)}")
