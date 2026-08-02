import json
from typing import Dict, Any

from app.ai.core.base_agent import BaseAgent
from app.ai.agents.explainability.schemas import (
    ExplainabilityAnalysisSchema,
    ExplainabilityAnalysis,
    AgentMetadata
)
from app.ai.agents.performance.utils import calculate_cost
from app.ai.agents.explainability.prompts.registry import PromptRegistry
from app.ai.agents.explainability.validators.schema_validator import SchemaValidator
from app.ai.agents.explainability.validators.business_validator import BusinessValidator
from app.ai.agents.explainability.utils import generate_prompt_hash, estimate_tokens
from app.ai.agents.explainability.exceptions import TokenLimitError, OutputValidationError
from config import settings

class ExplainabilityAgent(BaseAgent):
    """Enterprise Explainability Engine"""
    
    def __init__(self):
        super().__init__(
            provider_name="openai",
            model_name=settings.EXPLAINABILITY_AGENT_MODEL,
            temperature=settings.EXPLAINABILITY_AGENT_TEMPERATURE,
            max_tokens=settings.EXPLAINABILITY_AGENT_MAX_TOKENS,
            max_retries=settings.EXPLAINABILITY_AGENT_MAX_RETRIES
        )
        self.prompt_version = settings.EXPLAINABILITY_PROMPT_VERSION

    async def analyze(
        self, 
        context_bundle: Dict[str, Any],
        performance_analysis: Dict[str, Any],
        bias_analysis: Dict[str, Any],
        execution_id: str,
        workflow_id: str = None
    ) -> ExplainabilityAnalysis:
        
        system_prompt, developer_prompt = PromptRegistry.get_prompt_version(self.prompt_version)
        prompt_hash = generate_prompt_hash(system_prompt, developer_prompt)
        
        user_message = json.dumps({
            "context_bundle": context_bundle,
            "performance_analysis": performance_analysis,
            "bias_analysis": bias_analysis
        }, default=str)
        
        input_tokens = estimate_tokens(system_prompt + developer_prompt + user_message)
        if input_tokens > 100000:
            raise TokenLimitError(f"Inputs exceed max tokens: {input_tokens}")
            
        result = await self._execute_with_retry(
            system_prompt=system_prompt,
            developer_prompt=developer_prompt,
            user_message=user_message,
            response_model=ExplainabilityAnalysisSchema,
            execution_id=execution_id
        )
        
        raw_schema = result["parsed_data"]
        
        try:
            validated_schema = SchemaValidator.validate(raw_schema.model_dump())
            BusinessValidator.validate(validated_schema)
        except ValueError as e:
            raise OutputValidationError(str(e))
        
        cost_metrics = calculate_cost(result["model_used"], result["usage"])
        
        metadata = AgentMetadata(
            execution_id=execution_id,
            workflow_id=workflow_id,
            agent_version="1.0.0",
            prompt_version=self.prompt_version,
            prompt_hash=prompt_hash,
            model=result["model_used"],
            provider="openai",
            retries=0
        )
        
        return ExplainabilityAnalysis(
            analysis=validated_schema,
            cost_metrics=cost_metrics,
            metadata=metadata
        )
