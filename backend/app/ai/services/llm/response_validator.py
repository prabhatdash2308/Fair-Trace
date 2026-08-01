"""
Validates structured output from LLMs.
"""
import json
from pydantic import BaseModel, ValidationError
from typing import Type, Any
from .models import LLMResponse
from .exceptions import LLMValidationError

class ResponseValidator:
    @staticmethod
    def parse_and_validate(response: LLMResponse, schema: Type[BaseModel]) -> Any:
        try:
            # We assume response.content is a JSON string
            data = json.loads(response.content)
            validated = schema(**data)
            return validated
        except json.JSONDecodeError as e:
            raise LLMValidationError(f"Invalid JSON: {str(e)}") from e
        except ValidationError as e:
            raise LLMValidationError(f"Schema validation failed: {str(e)}") from e
