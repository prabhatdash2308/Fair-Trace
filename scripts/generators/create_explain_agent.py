import os
from pathlib import Path

agent_path = Path("backend/app/ai/agents/explainability_agent.py")
agent_path.parent.mkdir(parents=True, exist_ok=True)

content = '''"""
Explainability Agent for generating transparent reasoning traces.
"""
import time
from typing import List, Dict
from pydantic import BaseModel, Field

from app.ai.base.base_agent import BaseAgent
from app.ai.base.execution_context import ExecutionContext
from app.ai.state.review_state import ReviewState
from app.ai.base.exceptions import StateValidationError

from app.ai.services.llm import LLMService, LLMRequest
from app.ai.prompts import PromptRegistry, PromptMetadata

class ExplainabilityResult(BaseModel):
    executive_summary: str = Field(description="High level summary of the reasoning.")
    decision_path: List[str] = Field(description="Step-by-step path taken to reach conclusions.")
    competency_explanations: Dict[str, str] = Field(description="Explanations for each competency score.")
    bias_explanations: List[str] = Field(description="Explanations for how bias influenced the scoring.")
    confidence_explanation: str = Field(description="Reasoning for the confidence level.")
    citation_mapping: Dict[str, List[str]] = Field(description="Maps claims to their specific citations.")
    limitations: List[str] = Field(description="Any limitations or missing evidence noted.")

class ExplainabilityAgent(BaseAgent):
    """
    ExplainabilityAgent evaluates previous agent outputs and retrieved evidence 
    to provide clear, citation-backed reasoning traces.
    """
    def __init__(
        self, 
        llm_service: LLMService,
        prompt_registry: PromptRegistry,
        name: str = "ExplainabilityAgent", 
        max_retries: int = 3
    ):
        super().__init__(name=name, max_retries=max_retries)
        self.llm_service = llm_service
        self.prompt_registry = prompt_registry
        self._register_prompts()
        
    def _register_prompts(self):
        try:
            self.prompt_registry.get_prompt("explainability_prompt")
        except Exception:
            metadata = PromptMetadata(
                name="explainability_prompt",
                version="1.0",
                description="Explains AI conclusions using only supplied evidence.",
                owner_agent=self.name,
                required_variables=["employee_metadata", "analysis_result", "bias_findings", "supporting_citations"],
                system_prompt_path="system/explainability.txt",
                user_prompt_path="user/explainability.txt"
            )
            try:
                self.prompt_registry.register(metadata)
            except Exception:
                pass

    def _validate_before_process(self, state: ReviewState) -> None:
        if not state.analysis or state.analysis.status != "completed":
            raise StateValidationError("Performance analysis must be completed before explainability.")
            
    def _process(self, state: ReviewState, context: ExecutionContext) -> ReviewState:
        # 1. Validation
        self._validate_before_process(state)
        state.explainability.status = "processing"
        
        start_time = time.perf_counter()
        
        # 2. Gather Context
        employee_meta = f"Employee ID: {state.metadata.employee_id}"
        analysis_res = str(state.analysis.model_dump())
        bias_res = "\\n".join([f"[{f.bias_type.name}] {f.reason}" for f in state.bias.findings]) if hasattr(state, 'bias') and state.bias.findings else "No bias detected."
        citations = "\\n".join(state.analysis.supporting_citations)
        
        # 3. Render Prompts
        sys_prompt, user_prompt = self.prompt_registry.render_prompt(
            "explainability_prompt", 
            variables={
                "employee_metadata": employee_meta,
                "analysis_result": analysis_res,
                "bias_findings": bias_res,
                "supporting_citations": citations
            }
        )
        
        # 4. LLM Execution (Structured JSON Output)
        req = LLMRequest(
            system_prompt=sys_prompt,
            user_prompt=user_prompt,
            response_format=ExplainabilityResult,
            temperature=0.0 # Deterministic reasoning
        )
        
        res = self.llm_service.generate(req, correlation_id=context.correlation_id)
        structured_res: ExplainabilityResult = res.structured_data
        
        # 5. Populate State
        state.explainability.executive_summary = structured_res.executive_summary
        state.explainability.decision_path = structured_res.decision_path
        state.explainability.competency_explanations = structured_res.competency_explanations
        state.explainability.bias_explanations = structured_res.bias_explanations
        state.explainability.confidence_explanation = structured_res.confidence_explanation
        state.explainability.citation_mapping = structured_res.citation_mapping
        state.explainability.limitations = structured_res.limitations
        
        latency_ms = int((time.perf_counter() - start_time) * 1000)
        state.explainability.explainability_cost = res.cost if hasattr(res, 'cost') else 0.0
        state.explainability.explainability_latency_ms = latency_ms
        state.explainability.status = "completed"
        
        # 6. Audit & Execution Logs
        state.execution.completed_steps.append(self.name)
        state.audit.agent_logs.append(
            f"[{self.name}] Generated explainability trace. Cost: "
        )
        
        return state
'''
agent_path.write_text(content, encoding="utf-8")

# Prompts
sys_prompt = Path("backend/app/ai/prompts/system/explainability.txt")
sys_prompt.parent.mkdir(parents=True, exist_ok=True)
sys_prompt.write_text("Enterprise AI Explainability Specialist. Explain every conclusion using only supplied evidence. Never generate new evidence. Never change previous conclusions. Return STRICT JSON.", encoding="utf-8")

user_prompt = Path("backend/app/ai/prompts/user/explainability.txt")
user_prompt.parent.mkdir(parents=True, exist_ok=True)
user_prompt.write_text("Employee: {{employee_metadata}}\\nAnalysis: {{analysis_result}}\\nBias Context: {{bias_findings}}\\nCitations: {{supporting_citations}}\\nProvide the explainability trace.", encoding="utf-8")

print("ExplainabilityAgent created")
