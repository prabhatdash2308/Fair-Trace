import os
from pathlib import Path
import datetime

agent_path = Path("backend/app/ai/agents/human_approval_agent.py")
agent_path.parent.mkdir(parents=True, exist_ok=True)

content = '''"""
Human Approval Agent for orchestrating manual oversight of AI-generated reviews.
"""
import time
import datetime
from typing import List
from pydantic import BaseModel, Field

from app.ai.base.base_agent import BaseAgent
from app.ai.base.execution_context import ExecutionContext
from app.ai.state.review_state import ReviewState
from app.ai.base.exceptions import StateValidationError

from app.ai.services.llm import LLMService, LLMRequest
from app.ai.prompts import PromptRegistry, PromptMetadata

class ApprovalPreparationResult(BaseModel):
    approval_summary: str = Field(description="Summary for the human reviewer.")
    reviewer_checklist: List[str] = Field(description="List of items the reviewer should verify.")
    risk_flags: List[str] = Field(description="High severity bias or low confidence items.")
    pending_questions: List[str] = Field(description="Open questions needing human input.")
    recommended_action: str = Field(description="Agent's recommendation for the pipeline (e.g. Pause, Request Revision).")

class HumanApprovalAgent(BaseAgent):
    """
    HumanApprovalAgent prepares the final output for manual human review,
    determining if the workflow should pause based on bias, confidence, and completion rules.
    """
    def __init__(
        self, 
        llm_service: LLMService,
        prompt_registry: PromptRegistry,
        name: str = "HumanApprovalAgent", 
        max_retries: int = 3
    ):
        super().__init__(name=name, max_retries=max_retries)
        self.llm_service = llm_service
        self.prompt_registry = prompt_registry
        self._register_prompts()
        
    def _register_prompts(self):
        try:
            self.prompt_registry.get_prompt("human_approval_prompt")
        except Exception:
            metadata = PromptMetadata(
                name="human_approval_prompt",
                version="1.0",
                description="Prepares the review for human approval oversight.",
                owner_agent=self.name,
                required_variables=["report_summary", "confidence_summary", "bias_summary", "pending_risks"],
                system_prompt_path="system/human_approval.txt",
                user_prompt_path="user/human_approval.txt"
            )
            try:
                self.prompt_registry.register(metadata)
            except Exception:
                pass

    def _validate_before_process(self, state: ReviewState) -> None:
        if not state.report or state.report.status != "completed":
            raise StateValidationError("Report generation must be completed before human approval prep.")
            
    def _process(self, state: ReviewState, context: ExecutionContext) -> ReviewState:
        # 1. Validation
        self._validate_before_process(state)
        state.approval.status = "processing"
        
        start_time = time.perf_counter()
        
        # 2. Hardcoded Workflow Rules
        # Do not modify report, scores, or recommendations.
        # Just prepare the approval package.
        
        # 3. Gather Context
        report_summary = state.report.executive_summary
        conf_summary = state.report.confidence_summary
        bias_sum = state.report.bias_summary
        risks = "\\n".join(state.report.limitations) if state.report.limitations else "None."
        
        # 4. Render Prompts
        sys_prompt, user_prompt = self.prompt_registry.render_prompt(
            "human_approval_prompt", 
            variables={
                "report_summary": report_summary,
                "confidence_summary": conf_summary,
                "bias_summary": bias_sum,
                "pending_risks": risks
            }
        )
        
        # 5. LLM Execution (Structured JSON Output)
        req = LLMRequest(
            system_prompt=sys_prompt,
            user_prompt=user_prompt,
            response_format=ApprovalPreparationResult,
            temperature=0.0 # Deterministic checklist generation
        )
        
        res = self.llm_service.generate(req, correlation_id=context.correlation_id)
        structured_res: ApprovalPreparationResult = res.structured_data
        
        # 6. Populate State
        state.approval.approval_required = True
        state.approval.approval_status = "PENDING"
        state.approval.approval_summary = structured_res.approval_summary
        state.approval.reviewer_checklist = structured_res.reviewer_checklist
        state.approval.risk_flags = structured_res.risk_flags
        state.approval.pending_questions = structured_res.pending_questions
        state.approval.recommended_action = structured_res.recommended_action
        state.approval.submitted_at = datetime.datetime.utcnow().isoformat()
        
        latency_ms = int((time.perf_counter() - start_time) * 1000)
        state.approval.approval_cost = res.cost if hasattr(res, 'cost') else 0.0
        state.approval.approval_latency_ms = latency_ms
        state.approval.status = "completed"
        
        # 7. Audit & Execution Logs
        state.execution.completed_steps.append(self.name)
        state.audit.agent_logs.append(
            f"[{self.name}] Prepared human approval package. Cost: "
        )
        
        return state
'''
agent_path.write_text(content, encoding="utf-8")

# Prompts
sys_prompt = Path("backend/app/ai/prompts/system/human_approval.txt")
sys_prompt.parent.mkdir(parents=True, exist_ok=True)
sys_prompt.write_text("Enterprise HR Review Coordinator. Prepare a concise approval summary. Never rewrite report. Never generate new analysis. Return STRICT JSON.", encoding="utf-8")

user_prompt = Path("backend/app/ai/prompts/user/human_approval.txt")
user_prompt.parent.mkdir(parents=True, exist_ok=True)
user_prompt.write_text("Report: {{report_summary}}\\nConfidence: {{confidence_summary}}\\nBias: {{bias_summary}}\\nRisks: {{pending_risks}}\\nPrepare the human reviewer checklist.", encoding="utf-8")

print("HumanApprovalAgent created")
