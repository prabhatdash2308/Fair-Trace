from typing import Dict, Any
from app.ai.agents.performance.agent import PerformanceAgent
from app.ai.agents.performance.telemetry import emit_performance_telemetry, log_prompt_snapshot
from app.ai.agents.performance.prompts.registry import PromptRegistry

class PerformanceAnalysisService:
    """Domain service wrapping the AI Agent for LangGraph integration."""
    
    @staticmethod
    async def analyze_context(state: Dict[str, Any]) -> Dict[str, Any]:
        """Orchestrates the performance agent execution."""
        
        execution_id = state.get("execution_id")
        context_bundle = state.get("context_bundle")
        
        if not execution_id:
            raise ValueError("Execution ID is missing.")
        if not context_bundle:
            raise ValueError("Context bundle is missing.")
            
        agent = PerformanceAgent()
        
        # Record prompt snapshot in telemetry
        sys, dev = PromptRegistry.get_prompt_version(agent.prompt_version)
        from app.ai.agents.performance.utils import generate_prompt_hash
        log_prompt_snapshot(execution_id, sys, dev, generate_prompt_hash(sys, dev))
        
        # Execute Analysis
        analysis_result = await agent.analyze(context_bundle, execution_id)
        
        # Emit final telemetry
        emit_performance_telemetry(
            execution_id=execution_id,
            workflow_id=state.get("workflow_id"),
            metadata=analysis_result.metadata.model_dump(),
            cost_metrics=analysis_result.cost_metrics.model_dump()
        )
        
        return analysis_result.model_dump()
    
    @staticmethod
    def get_health() -> Dict[str, Any]:
        agent = PerformanceAgent()
        health = agent.health()
        return {
            "provider": "OpenAI",
            "model": agent.model_name,
            "prompt_version": agent.prompt_version,
            "provider_status": health["provider_status"],
            "configuration": "valid",
            "last_successful_call": "TBD" # Can be wired to a DB or cache if needed
        }
