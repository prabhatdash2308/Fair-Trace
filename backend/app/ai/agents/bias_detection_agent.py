"""
Bias Detection Agent for analyzing evidence and surfacing biases.
"""
import time
from typing import List
from pydantic import BaseModel, Field

from app.ai.base.base_agent import BaseAgent
from app.ai.base.execution_context import ExecutionContext
from app.ai.state.review_state import ReviewState, BiasFinding, BiasType, BiasSeverity
from app.ai.base.exceptions import StateValidationError

from app.ai.services.llm import LLMService, LLMRequest
from app.ai.prompts import PromptRegistry, PromptMetadata

class BiasDetectionResult(BaseModel):
    status: str = Field(description="Must be 'SUCCESS' or 'NOT_ENOUGH_EVIDENCE'")
    findings: List[BiasFinding] = Field(default_factory=list)

class BiasDetectionAgent(BaseAgent):
    """
    BiasDetectionAgent uses an LLM to evaluate retrieved evidence for 
    various performance review biases, without hallucination.
    """
    def __init__(
        self, 
        llm_service: LLMService,
        prompt_registry: PromptRegistry,
        name: str = "BiasDetectionAgent", 
        max_retries: int = 3
    ):
        super().__init__(name=name, max_retries=max_retries)
        self.llm_service = llm_service
        self.prompt_registry = prompt_registry
        self._register_prompts()
        
    def _register_prompts(self):
        try:
            self.prompt_registry.get_prompt("bias_detection_prompt")
        except Exception:
            metadata = PromptMetadata(
                name="bias_detection_prompt",
                version="1.0",
                description="Detects biases based ONLY on retrieved evidence.",
                owner_agent=self.name,
                required_variables=["evidence"],
                system_prompt_path="system/bias.txt",
                user_prompt_path="user/bias.txt"
            )
            try:
                self.prompt_registry.register(metadata)
            except Exception as e:
                pass # Already registered or error

    def _validate_before_process(self, state: ReviewState) -> None:
        if not state.evidence or state.evidence.status != "completed":
            raise StateValidationError("Evidence retrieval has not been completed.")
            
    def _process(self, state: ReviewState, context: ExecutionContext) -> ReviewState:
        # 1. Validation
        self._validate_before_process(state)
        state.bias.status = "processing"
        
        start_time = time.perf_counter()
        
        # 2. Gather Evidence
        citations = state.evidence.citations
        if not citations:
            state.audit.warnings.append(f"[{self.name}] No evidence found in state. Skipping bias detection.")
            state.bias.status = "completed"
            return state
            
        evidence_text = "\n".join(citations)
        
        # 3. Render Prompts
        sys_prompt, user_prompt = self.prompt_registry.render_prompt(
            "bias_detection_prompt", 
            variables={"evidence": evidence_text}
        )
        
        # 4. LLM Execution (Structured JSON Output)
        req = LLMRequest(
            system_prompt=sys_prompt,
            user_prompt=user_prompt,
            response_format=BiasDetectionResult,
            temperature=0.0 # Deterministic reasoning
        )
        
        res = self.llm_service.generate(req, correlation_id=context.correlation_id)
        structured_res: BiasDetectionResult = res.structured_data
        
        # 5. Populate State
        if structured_res.status == "NOT_ENOUGH_EVIDENCE":
            state.audit.warnings.append(f"[{self.name}] LLM returned NOT_ENOUGH_EVIDENCE.")
        else:
            state.bias.findings = structured_res.findings
            # Legacy fields update
            for f in structured_res.findings:
                state.bias.bias_types.append(f.bias_type)
                state.bias.bias_flags.append(f.reason)
                
        latency_ms = int((time.perf_counter() - start_time) * 1000)
        state.bias.status = "completed"
        
        # 6. Audit & Execution Logs
        state.execution.completed_steps.append(self.name)
        state.audit.agent_logs.append(
            f"[{self.name}] Evaluated {len(citations)} citations. Found {len(structured_res.findings)} biases. Cost: "
        )
        
        return state
