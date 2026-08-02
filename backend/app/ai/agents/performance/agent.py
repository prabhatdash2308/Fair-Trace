import json
from typing import Dict, Any

from app.ai.core.base_agent import BaseAgent
from app.ai.agents.performance.schemas import (
    PerformanceAnalysisSchema,
    PerformanceAnalysis,
    AgentMetadata
)
from app.ai.agents.performance.prompts.registry import PromptRegistry
from app.ai.agents.performance.validators.schema_validator import SchemaValidator
from app.ai.agents.performance.validators.business_validator import BusinessValidator
from app.ai.agents.performance.utils import calculate_cost, generate_prompt_hash, estimate_tokens
from app.ai.agents.performance.exceptions import TokenLimitError
from config import settings

class PerformanceAgent(BaseAgent):
    """Enterprise Performance Analysis Agent"""
    
    def __init__(self):
        super().__init__(
            provider_name="openai",
            model_name=settings.PERFORMANCE_AGENT_MODEL,
            temperature=settings.PERFORMANCE_AGENT_TEMPERATURE,
            max_tokens=settings.PERFORMANCE_AGENT_MAX_TOKENS,
            max_retries=settings.PERFORMANCE_AGENT_MAX_RETRIES
        )
        self.prompt_version = settings.PERFORMANCE_PROMPT_VERSION

    async def analyze(
        self, 
        context_bundle: Dict[str, Any], 
        execution_id: str,
        workflow_id: str = None
    ) -> PerformanceAnalysis:
        
        # 1. Fetch Prompts
        system_prompt, developer_prompt = PromptRegistry.get_prompt_version(self.prompt_version)
        prompt_hash = generate_prompt_hash(system_prompt, developer_prompt)
        
        # 2. Format Context
        user_message = json.dumps(context_bundle, default=str)
        
        # 3. Guardrails: Token checking (Fail fast)
        input_tokens = estimate_tokens(system_prompt + developer_prompt + user_message)
        if input_tokens > 100000: # Example safeguard
            raise TokenLimitError(f"Context bundle exceeds max tokens: {input_tokens}")
            
        # 4. Execute LLM Call (Includes retry mechanism)
        result = await self._execute_with_retry(
            system_prompt=system_prompt,
            developer_prompt=developer_prompt,
            user_message=user_message,
            response_model=PerformanceAnalysisSchema,
            execution_id=execution_id
        )
        
        raw_schema = result["parsed_data"]
        
        # 5. Validate Outputs
        validated_schema = SchemaValidator.validate(raw_schema.model_dump())
        BusinessValidator.validate(validated_schema)
        
        # 6. Accounting & Telemetry
        cost_metrics = calculate_cost(result["model_used"], result["usage"])
        
        metadata = AgentMetadata(
            execution_id=execution_id,
            workflow_id=workflow_id,
            agent_version="1.0.0",
            prompt_version=self.prompt_version,
            prompt_hash=prompt_hash,
            model=result["model_used"],
            provider="openai",
            retries=0 # Actually, we might need to track retries from the base loop in a more advanced way
        )
        
        return PerformanceAnalysis(
            analysis=validated_schema,
            cost_metrics=cost_metrics,
            metadata=metadata
        )
