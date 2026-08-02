from typing import Dict, Any
from app.ai.agents.bias.agent import BiasAgent
from app.ai.agents.bias.telemetry import emit_bias_telemetry, log_prompt_snapshot
from app.ai.agents.bias.prompts.registry import PromptRegistry
from app.ai.agents.bias.enums import BiasSeverity

class BiasAnalysisService:
    """Domain service wrapping the Bias Agent for LangGraph integration."""
    
    @staticmethod
    async def analyze_context(state: Dict[str, Any]) -> Dict[str, Any]:
        """Orchestrates the bias agent execution."""
        
        execution_id = state.get("execution_id")
        context_bundle = state.get("context_bundle")
        performance_analysis = state.get("performance_analysis")
        
        if not execution_id:
            raise ValueError("Execution ID is missing.")
        if not context_bundle:
            raise ValueError("Context bundle is missing.")
        if not performance_analysis:
            raise ValueError("Performance analysis is missing.")
            
        agent = BiasAgent()
        
        # Record prompt snapshot in telemetry
        sys, dev = PromptRegistry.get_prompt_version(agent.prompt_version)
        from app.ai.agents.bias.utils import generate_prompt_hash
        log_prompt_snapshot(execution_id, sys, dev, generate_prompt_hash(sys, dev))
        
        # Execute Analysis
        analysis_result = await agent.analyze(context_bundle, performance_analysis, execution_id)
        
        # Calculate extra metrics for telemetry
        biases = analysis_result.analysis.detected_biases
        bias_count = len(biases)
        high_severity_count = sum(1 for b in biases if b.severity == BiasSeverity.HIGH)
        critical_severity_count = sum(1 for b in biases if b.severity == BiasSeverity.CRITICAL)
        unsupported_claims_count = len(analysis_result.analysis.unsupported_claims)
        missing_evidence_count = len(analysis_result.analysis.missing_evidence)
        
        # Emit final telemetry
        emit_bias_telemetry(
            execution_id=execution_id,
            workflow_id=state.get("workflow_id"),
            metadata=analysis_result.metadata.model_dump(),
            cost_metrics=analysis_result.cost_metrics.model_dump(),
            bias_score=analysis_result.analysis.overall_bias_score,
            risk_level=analysis_result.analysis.risk_level.value,
            bias_count=bias_count,
            high_severity_count=high_severity_count,
            critical_severity_count=critical_severity_count,
            unsupported_claims_count=unsupported_claims_count,
            missing_evidence_count=missing_evidence_count
        )
        
        return analysis_result.model_dump()
    
    @staticmethod
    def get_health() -> Dict[str, Any]:
        agent = BiasAgent()
        health = agent.health()
        
        # Snapshot for health endpoint
        sys, dev = PromptRegistry.get_prompt_version(agent.prompt_version)
        from app.ai.agents.bias.utils import generate_prompt_hash
        prompt_hash = generate_prompt_hash(sys, dev)
        
        return {
            "provider": "OpenAI",
            "model": agent.model_name,
            "prompt_version": agent.prompt_version,
            "prompt_hash": prompt_hash,
            "status": health["provider_status"],
            "configuration": "valid"
        }
