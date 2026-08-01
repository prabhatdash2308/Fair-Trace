import os
from pathlib import Path
import datetime

agent_path = Path("backend/app/ai/agents/report_generation_agent.py")
agent_path.parent.mkdir(parents=True, exist_ok=True)

content = '''"""
Report Generation Agent for producing the final HR review artifact.
"""
import time
import datetime
from typing import List, Dict
from pydantic import BaseModel, Field

from app.ai.base.base_agent import BaseAgent
from app.ai.base.execution_context import ExecutionContext
from app.ai.state.review_state import ReviewState
from app.ai.base.exceptions import StateValidationError

from app.ai.services.llm import LLMService, LLMRequest
from app.ai.prompts import PromptRegistry, PromptMetadata

class PerformanceReportResult(BaseModel):
    executive_summary: str = Field(description="High level executive summary of the review.")
    employee_overview: str = Field(description="Basic overview of the employee's standing.")
    performance_summary: str = Field(description="Summary of core performance.")
    strengths: List[str] = Field(description="Key strengths.")
    areas_for_improvement: List[str] = Field(description="Key areas for growth.")
    competency_breakdown: Dict[str, float] = Field(description="Detailed competency scores.")
    bias_summary: str = Field(description="Summary of any bias detected and mitigated.")
    confidence_summary: str = Field(description="Summary of system confidence in the evaluation.")
    recommendations: List[str] = Field(description="Actionable recommendations.")
    supporting_citations: List[str] = Field(description="Citations extracted from evidence supporting the report.")
    limitations: List[str] = Field(description="Limitations of the review.")

class ReportGenerationAgent(BaseAgent):
    """
    ReportGenerationAgent transforms structured analysis into a final,
    professional HR performance review document.
    """
    def __init__(
        self, 
        llm_service: LLMService,
        prompt_registry: PromptRegistry,
        name: str = "ReportGenerationAgent", 
        max_retries: int = 3
    ):
        super().__init__(name=name, max_retries=max_retries)
        self.llm_service = llm_service
        self.prompt_registry = prompt_registry
        self._register_prompts()
        
    def _register_prompts(self):
        try:
            self.prompt_registry.get_prompt("report_generation_prompt")
        except Exception:
            metadata = PromptMetadata(
                name="report_generation_prompt",
                version="1.0",
                description="Generates a professional HR review report from structured outputs.",
                owner_agent=self.name,
                required_variables=["employee_metadata", "analysis", "bias_summary", "explainability", "citations"],
                system_prompt_path="system/report_generation.txt",
                user_prompt_path="user/report_generation.txt"
            )
            try:
                self.prompt_registry.register(metadata)
            except Exception:
                pass

    def _validate_before_process(self, state: ReviewState) -> None:
        if not state.explainability or state.explainability.status != "completed":
            raise StateValidationError("Explainability trace must be completed before report generation.")
            
    def _process(self, state: ReviewState, context: ExecutionContext) -> ReviewState:
        # 1. Validation
        self._validate_before_process(state)
        state.report.status = "processing"
        
        start_time = time.perf_counter()
        
        # 2. Gather Context
        employee_meta = f"Employee ID: {state.metadata.employee_id}"
        analysis_res = str(state.analysis.model_dump())
        bias_res = str(state.bias.model_dump())
        explain_res = str(state.explainability.model_dump())
        citations = "\\n".join(state.analysis.supporting_citations)
        
        # 3. Render Prompts
        sys_prompt, user_prompt = self.prompt_registry.render_prompt(
            "report_generation_prompt", 
            variables={
                "employee_metadata": employee_meta,
                "analysis": analysis_res,
                "bias_summary": bias_res,
                "explainability": explain_res,
                "citations": citations
            }
        )
        
        # 4. LLM Execution (Structured JSON Output)
        req = LLMRequest(
            system_prompt=sys_prompt,
            user_prompt=user_prompt,
            response_format=PerformanceReportResult,
            temperature=0.0 # Deterministic reporting
        )
        
        res = self.llm_service.generate(req, correlation_id=context.correlation_id)
        structured_res: PerformanceReportResult = res.structured_data
        
        # 5. Populate State
        state.report.report_title = f"Performance Review: {state.metadata.employee_id}"
        state.report.executive_summary = structured_res.executive_summary
        state.report.employee_overview = structured_res.employee_overview
        state.report.performance_summary = structured_res.performance_summary
        state.report.strengths = structured_res.strengths
        state.report.areas_for_improvement = structured_res.areas_for_improvement
        state.report.competency_breakdown = structured_res.competency_breakdown
        state.report.bias_summary = structured_res.bias_summary
        state.report.confidence_summary = structured_res.confidence_summary
        state.report.recommendations = structured_res.recommendations
        state.report.supporting_citations = structured_res.supporting_citations
        state.report.limitations = structured_res.limitations
        state.report.generated_at = datetime.datetime.utcnow().isoformat()
        
        latency_ms = int((time.perf_counter() - start_time) * 1000)
        state.report.report_cost = res.cost if hasattr(res, 'cost') else 0.0
        state.report.report_latency_ms = latency_ms
        state.report.status = "completed"
        
        # 6. Audit & Execution Logs
        state.execution.completed_steps.append(self.name)
        state.audit.agent_logs.append(
            f"[{self.name}] Generated performance report. Cost: "
        )
        
        return state
'''
agent_path.write_text(content, encoding="utf-8")

# Prompts
sys_prompt = Path("backend/app/ai/prompts/system/report_generation.txt")
sys_prompt.parent.mkdir(parents=True, exist_ok=True)
sys_prompt.write_text("Enterprise Performance Report Writer. Generate a professional HR review. Never introduce new conclusions. Never invent evidence. Never alter competency scores. Never alter confidence values. Return STRICT JSON only.", encoding="utf-8")

user_prompt = Path("backend/app/ai/prompts/user/report_generation.txt")
user_prompt.parent.mkdir(parents=True, exist_ok=True)
user_prompt.write_text("Employee: {{employee_metadata}}\\nAnalysis: {{analysis}}\\nBias: {{bias_summary}}\\nExplainability: {{explainability}}\\nCitations: {{citations}}\\nGenerate professional report.", encoding="utf-8")

print("ReportGenerationAgent created")
