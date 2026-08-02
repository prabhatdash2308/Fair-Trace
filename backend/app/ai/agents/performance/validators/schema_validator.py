from typing import Any, Dict
from pydantic import ValidationError
from app.ai.agents.performance.schemas import PerformanceAnalysisSchema
from app.ai.agents.performance.exceptions import OutputValidationError

class SchemaValidator:
    """Validates raw output dictionaries against the strict Pydantic schema."""
    
    @staticmethod
    def validate(raw_data: Dict[str, Any]) -> PerformanceAnalysisSchema:
        try:
            return PerformanceAnalysisSchema.model_validate(raw_data)
        except ValidationError as e:
            raise OutputValidationError(f"Schema validation failed: {str(e)}")
