import json
from typing import Dict, Any
import datetime

from app.ai.core.base_agent import BaseAgent
from app.ai.agents.report.schemas import (
    EnterprisePerformanceReportSchema,
    EnterprisePerformanceReport,
    ReportMetadata,
    AuditSummary,
    PipelineMetrics
)
from app.ai.agents.performance.utils import calculate_cost
from app.ai.agents.report.prompts.registry import PromptRegistry
from app.ai.agents.report.validators.schema_validator import SchemaValidator
from app.ai.agents.report.validators.business_validator import BusinessValidator
from app.ai.agents.report.utils import generate_prompt_hash, estimate_tokens
from app.ai.agents.report.exceptions import TokenLimitError, OutputValidationError
from config import settings

class ReportGenerationAgent(BaseAgent):
    """Enterprise Report Generation Engine"""
    
    def __init__(self):
        super().__init__(
            provider_name="openai",
            model_name=settings.REPORT_AGENT_MODEL,
            temperature=settings.REPORT_AGENT_TEMPERATURE,
            max_tokens=settings.REPORT_AGENT_MAX_TOKENS,
            max_retries=settings.REPORT_AGENT_MAX_RETRIES
        )
        self.prompt_version = settings.REPORT_PROMPT_VERSION

    async def generate(
        self, 
        context_bundle: Dict[str, Any],
        performance_analysis: Dict[str, Any],
        bias_analysis: Dict[str, Any],
        explainability_analysis: Dict[str, Any],
        execution_id: str,
        workflow_id: str = None
    ) -> Dict[str, Any]:
        
        system_prompt, developer_prompt = PromptRegistry.get_prompt_version(self.prompt_version)
        prompt_hash = generate_prompt_hash(system_prompt, developer_prompt)
        
        user_message = json.dumps({
            "context_bundle": context_bundle,
            "performance_analysis": performance_analysis,
            "bias_analysis": bias_analysis,
            "explainability_analysis": explainability_analysis
        }, default=str)
        
        input_tokens = estimate_tokens(system_prompt + developer_prompt + user_message)
        if input_tokens > 100000:
            raise TokenLimitError(f"Inputs exceed max tokens: {input_tokens}")
            
        result = await self._execute_with_retry(
            system_prompt=system_prompt,
            developer_prompt=developer_prompt,
            user_message=user_message,
            response_model=EnterprisePerformanceReportSchema,
            execution_id=execution_id
        )
        
        raw_schema = result["parsed_data"]
        
        try:
            validated_schema = SchemaValidator.validate(raw_schema.model_dump())
            BusinessValidator.validate(validated_schema)
        except ValueError as e:
            raise OutputValidationError(str(e))
        
        cost_metrics = calculate_cost(result["model_used"], result["usage"])
        
        # Pipeline Aggregation
        perf_cost = performance_analysis.get("cost_metrics", {}).get("total_cost", 0.0)
        bias_cost = bias_analysis.get("bias_cost", {}).get("total_cost", 0.0)
        expl_cost = explainability_analysis.get("cost_metrics", {}).get("total_cost", 0.0)
        total_pipeline_cost = perf_cost + bias_cost + expl_cost + cost_metrics.total_cost
        
        metadata = ReportMetadata(
            report_version="1.0",
            schema_version="1.0",
            prompt_version=self.prompt_version,
            prompt_hash=prompt_hash,
            model=result["model_used"],
            provider="openai",
            execution_id=execution_id,
            workflow_id=workflow_id or "",
            generated_at=datetime.datetime.utcnow().isoformat() + "Z"
        )
        
        audit_summary = AuditSummary(
            performance_confidence=performance_analysis.get("analysis", {}).get("overall_score_confidence", 0.0),
            bias_summary=f"Detected {len(bias_analysis.get('bias_analysis', {}).get('detected_biases', []))} biases",
            explainability_coverage=explainability_analysis.get("analysis", {}).get("transparency_metrics", {}).get("coverage", 0.0),
            evidence_count=len(explainability_analysis.get("analysis", {}).get("evidence_map", [])),
            prompt_version=self.prompt_version,
            prompt_hash=prompt_hash,
            model=result["model_used"],
            execution_id=execution_id,
            workflow_id=workflow_id or "",
            generated_at=metadata.generated_at
        )
        
        pipeline_metrics = PipelineMetrics(
            total_pipeline_cost=total_pipeline_cost,
            total_tokens=cost_metrics.total_tokens,
            report_length=len(json.dumps(validated_schema.model_dump())),
            recommendation_count=len(validated_schema.recommended_actions),
            strength_count=len(validated_schema.strengths),
            improvement_count=len(validated_schema.improvement_areas),
            evidence_count=audit_summary.evidence_count,
            risk_count=validated_schema.risk_summary.unsupported_claims + validated_schema.risk_summary.missing_evidence,
            overall_score=validated_schema.overall_rating,
            confidence=validated_schema.overall_confidence
        )
        
        final_report = EnterprisePerformanceReport(
            report=validated_schema,
            audit_summary=audit_summary,
            pipeline_metrics=pipeline_metrics,
            cost_metrics=cost_metrics,
            metadata=metadata
        )
        
        return final_report.model_dump()
