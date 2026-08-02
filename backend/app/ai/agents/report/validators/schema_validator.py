from typing import Any, Dict
from pydantic import ValidationError
from app.ai.agents.report.schemas import EnterprisePerformanceReportSchema

class SchemaValidator:
    @staticmethod
    def validate(raw_data: Dict[str, Any]) -> EnterprisePerformanceReportSchema:
        try:
            return EnterprisePerformanceReportSchema.model_validate(raw_data)
        except ValidationError as e:
            raise ValueError(f"Schema validation failed: {str(e)}")
