import time
import structlog
from typing import Any, Dict, Optional, Type
from pydantic import BaseModel

from app.ai.core.provider_registry import ProviderRegistry

logger = structlog.get_logger(__name__)

class BaseAgent:
    """Base generic class for all enterprise AI Agents."""
    
    def __init__(
        self,
        provider_name: str,
        model_name: str,
        temperature: float,
        max_tokens: int,
        max_retries: int
    ):
        self.provider = ProviderRegistry.get_provider(provider_name)
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.max_retries = max_retries
        
    async def _execute_with_retry(
        self,
        system_prompt: str,
        developer_prompt: str,
        user_message: str,
        response_model: Type[BaseModel],
        execution_id: str
    ) -> Dict[str, Any]:
        """Executes LLM call with built-in retry safety and generic telemetry."""
        
        last_exception = None
        
        for attempt in range(1, self.max_retries + 2): # 1 initial + max_retries
            start_time = time.monotonic()
            try:
                result = await self.provider.generate_structured(
                    system_prompt=system_prompt,
                    developer_prompt=developer_prompt,
                    user_message=user_message,
                    response_model=response_model,
                    model_name=self.model_name,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                
                latency = time.monotonic() - start_time
                
                # Emit core execution telemetry
                logger.info(
                    "agent_execution_success",
                    execution_id=execution_id,
                    agent_class=self.__class__.__name__,
                    model=self.model_name,
                    attempt=attempt,
                    latency_s=round(latency, 3),
                    prompt_tokens=result["usage"]["prompt_tokens"],
                    completion_tokens=result["usage"]["completion_tokens"],
                    total_tokens=result["usage"]["total_tokens"]
                )
                
                return result
                
            except Exception as e:
                latency = time.monotonic() - start_time
                last_exception = e
                logger.warning(
                    "agent_execution_retry",
                    execution_id=execution_id,
                    agent_class=self.__class__.__name__,
                    model=self.model_name,
                    attempt=attempt,
                    latency_s=round(latency, 3),
                    error=str(e)
                )
                
        logger.error(
            "agent_execution_failed",
            execution_id=execution_id,
            agent_class=self.__class__.__name__,
            model=self.model_name,
            max_retries=self.max_retries,
            error=str(last_exception)
        )
        raise RuntimeError(f"{self.__class__.__name__} failed after {self.max_retries} retries: {str(last_exception)}")
        
    def health(self) -> Dict[str, str]:
        """Returns the health status of the agent's provider."""
        try:
            status = self.provider.health()
            return {
                "provider_status": status,
                "model": self.model_name
            }
        except Exception as e:
            return {
                "provider_status": f"unhealthy: {str(e)}",
                "model": self.model_name
            }
