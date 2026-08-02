from typing import Dict, Any
from app.ai.agents.explainability.agent import ExplainabilityAgent
from app.ai.agents.explainability.telemetry import emit_explainability_telemetry, log_prompt_snapshot
from app.ai.agents.explainability.prompts.registry import PromptRegistry

class ExplainabilityAnalysisService:
    @staticmethod
    async def analyze_context(state: Dict[str, Any]) -> Dict[str, Any]:
        execution_id = state.get("execution_id")
        context_bundle = state.get("context_bundle")
        performance_analysis = state.get("performance_analysis")
        bias_analysis = state.get("bias_analysis")
        
        if not execution_id:
            raise ValueError("Execution ID is missing.")
        if not context_bundle:
            raise ValueError("Context bundle is missing.")
        if not performance_analysis:
            raise ValueError("Performance analysis is missing.")
        if not bias_analysis:
            raise ValueError("Bias analysis is missing.")
            
        agent = ExplainabilityAgent()
        
        sys, dev = PromptRegistry.get_prompt_version(agent.prompt_version)
        from app.ai.agents.explainability.utils import generate_prompt_hash
        log_prompt_snapshot(execution_id, sys, dev, generate_prompt_hash(sys, dev))
        
        analysis_result = await agent.analyze(context_bundle, performance_analysis, bias_analysis, execution_id)
        
        # Telemetry metrics extraction
        metrics = analysis_result.analysis.transparency_metrics
        reasoning_count = len(analysis_result.analysis.reasoning_trace)
        
        emit_explainability_telemetry(
            execution_id=execution_id,
            workflow_id=state.get("workflow_id"),
            metadata=analysis_result.metadata.model_dump(),
            cost_metrics=analysis_result.cost_metrics.model_dump(),
            reasoning_step_count=reasoning_count,
            evidence_count=len(analysis_result.analysis.evidence_map),
            coverage=metrics.coverage,
            unsupported_claims_count=metrics.unsupported_claims_count,
            bias_adjustments_count=metrics.bias_adjustments_count,
            average_confidence=analysis_result.analysis.overall_confidence
        )
        
        return analysis_result.model_dump()
    
    @staticmethod
    def get_health() -> Dict[str, Any]:
        agent = ExplainabilityAgent()
        health = agent.health()
        
        sys, dev = PromptRegistry.get_prompt_version(agent.prompt_version)
        from app.ai.agents.explainability.utils import generate_prompt_hash
        
        return {
            "provider": "OpenAI",
            "model": agent.model_name,
            "prompt_version": agent.prompt_version,
            "prompt_hash": generate_prompt_hash(sys, dev),
            "status": health["provider_status"],
            "configuration": "valid"
        }
