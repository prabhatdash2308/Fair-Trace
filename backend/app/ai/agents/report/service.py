from typing import Dict, Any
from app.ai.agents.report.agent import ReportGenerationAgent
from app.ai.agents.report.telemetry import emit_report_telemetry, log_prompt_snapshot
from app.ai.agents.report.prompts.registry import PromptRegistry

class ReportGenerationService:
    @staticmethod
    async def generate_report(state: Dict[str, Any]) -> Dict[str, Any]:
        execution_id = state.get("execution_id")
        context_bundle = state.get("context_bundle")
        performance_analysis = state.get("performance_analysis")
        bias_analysis = state.get("bias_analysis")
        explainability_analysis = state.get("explainability_analysis")
        
        if not execution_id:
            raise ValueError("Execution ID is missing.")
        if not context_bundle:
            raise ValueError("Context bundle is missing.")
        if not performance_analysis:
            raise ValueError("Performance analysis is missing.")
        if not bias_analysis:
            raise ValueError("Bias analysis is missing.")
        if not explainability_analysis:
            raise ValueError("Explainability analysis is missing.")
            
        agent = ReportGenerationAgent()
        
        sys, dev = PromptRegistry.get_prompt_version(agent.prompt_version)
        from app.ai.agents.report.utils import generate_prompt_hash
        log_prompt_snapshot(execution_id, sys, dev, generate_prompt_hash(sys, dev))
        
        report_data = await agent.generate(
            context_bundle, 
            performance_analysis, 
            bias_analysis, 
            explainability_analysis,
            execution_id,
            state.get("workflow_id")
        )
        
        # Telemetry metrics extraction
        metrics = report_data["pipeline_metrics"]
        
        emit_report_telemetry(
            execution_id=execution_id,
            workflow_id=state.get("workflow_id", ""),
            metadata=report_data["metadata"],
            cost_metrics=report_data["cost_metrics"],
            report_length=metrics["report_length"],
            recommendation_count=metrics["recommendation_count"],
            strength_count=metrics["strength_count"],
            improvement_count=metrics["improvement_count"],
            risk_count=metrics["risk_count"],
            evidence_count=metrics["evidence_count"],
            overall_score=metrics["overall_score"],
            confidence=metrics["confidence"]
        )
        
        return report_data
    
    @staticmethod
    def get_health() -> Dict[str, Any]:
        agent = ReportGenerationAgent()
        health = agent.health()
        
        sys, dev = PromptRegistry.get_prompt_version(agent.prompt_version)
        from app.ai.agents.report.utils import generate_prompt_hash
        
        return {
            "provider": "OpenAI",
            "model": agent.model_name,
            "prompt_version": agent.prompt_version,
            "prompt_hash": generate_prompt_hash(sys, dev),
            "status": health["provider_status"],
            "configuration": "valid"
        }
