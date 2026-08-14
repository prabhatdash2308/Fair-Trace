"""
Performance Analysis Agent for generating evidence-based competency evaluations.
"""
import time
from typing import List, Dict
from pydantic import BaseModel, Field

from app.ai.base.base_agent import BaseAgent
from app.ai.base.execution_context import ExecutionContext
from app.ai.state.review_state import ReviewState
from app.ai.base.exceptions import StateValidationError

def _calculate_confidence(state: dict) -> dict:
    """
    Calculates a deterministic confidence score based on the amount of evidence,
    its relevance (similarity), diversity of sources, and penalizes for bias.
    """
    evidence_index = state.get("evidence_index", [])
    evidence_count = len(evidence_index)
    
    if evidence_count == 0:
        return {
            "score": "INSUFFICIENT",
            "numeric_score": 0.0,
            "explanation": "No evidence was found to support the analysis."
        }
        
    avg_sim = sum(e.get("similarity_score", 0.0) for e in evidence_index) / evidence_count if evidence_count > 0 else 0.0
    input_types = len({v.get("input_type") for v in state.get("validated_inputs", [])})
    
    # Base score built from evidence quality and diversity
    base_score = 0.0
    base_score += min(evidence_count * 0.1, 0.4) # Up to 0.4 for volume
    base_score += min(avg_sim * 0.4, 0.4)        # Up to 0.4 for relevance
    base_score += min(input_types * 0.1, 0.2)    # Up to 0.2 for diversity
    
    # Penalties for bias
    high_bias = state.get("high_bias_count", 0)
    medium_bias = state.get("medium_bias_count", 0)
    
    penalty = (high_bias * 0.15) + (medium_bias * 0.05)
    
    final_score = max(0.0, min(1.0, base_score - penalty))
    
    if final_score >= 0.7:
        score_label = "HIGH"
    elif final_score >= 0.5:
        score_label = "MEDIUM"
    elif final_score >= 0.3:
        score_label = "LOW"
    else:
        score_label = "INSUFFICIENT"
        
    return {
        "score": score_label,
        "numeric_score": final_score,
        "explanation": f"Computed from {evidence_count} evidence items with average similarity {avg_sim:.2f}, spanning {input_types} source types, penalized by {high_bias} high biases."
    }

def _calculate_performance_score(state: ReviewState, competencies: Dict[str, float]) -> float:
    """
    Deterministically calculates the overall performance score.
    Does NOT base the score only on evidence coverage; uses LLM competency evaluation
    and applies explicit, deterministic bias penalties (e.g., RECENCY -> -3.0).
    """
    if not competencies:
        return 0.0
        
    base_score = sum(competencies.values()) / len(competencies)
    
    # Explicit bias penalties
    bias_penalty_map = {
        "RECENCY": 3.0,
        "HALO": 5.0,
        "HORN": 5.0,
        "LENIENCY": 4.0,
        "SEVERITY": 4.0,
        "IMBALANCE": 2.0,
        "UNSUPPORTED": 5.0
    }
    
    total_penalty = 0.0
    if hasattr(state, 'bias') and state.bias.findings:
        for finding in state.bias.findings:
            b_type = finding.bias_type.name if hasattr(finding.bias_type, "name") else str(finding.bias_type).split(".")[-1]
            penalty = bias_penalty_map.get(b_type.upper(), 2.0)
            
            # Severity multiplier
            severity = finding.severity.name if hasattr(finding.severity, "name") else str(finding.severity).split(".")[-1]
            if severity.upper() == "HIGH":
                penalty *= 1.5
            elif severity.upper() == "LOW":
                penalty *= 0.5
                
            total_penalty += penalty
            
    final_score = max(0.0, min(100.0, base_score - total_penalty))
    return final_score

from app.ai.services.llm import LLMService, LLMRequest
from app.ai.prompts import PromptRegistry, PromptMetadata

class PerformanceAnalysisResult(BaseModel):
    strengths: List[str] = Field(description="List of observed strengths.")
    improvements: List[str] = Field(description="List of areas for improvement.")
    competencies: Dict[str, float] = Field(description="Key competencies and their scores (0-100).")
    overall_summary: str = Field(description="High level summary.")
    confidence: float = Field(description="Confidence score (0-100).")
    supporting_citations: List[str] = Field(description="Citations extracted from evidence.")
    reasoning: str = Field(description="Step by step reasoning for the evaluation.")

class PerformanceAnalysisAgent(BaseAgent):
    """
    PerformanceAnalysisAgent evaluates retrieved evidence to synthesize
    a performance analysis grounded strictly in facts.
    """
    def __init__(
        self, 
        llm_service: LLMService,
        prompt_registry: PromptRegistry,
        name: str = "PerformanceAnalysisAgent", 
        max_retries: int = 3
    ):
        super().__init__(name=name, max_retries=max_retries)
        self.llm_service = llm_service
        self.prompt_registry = prompt_registry
        self._register_prompts()
        
    def _register_prompts(self):
        try:
            self.prompt_registry.get_prompt("performance_analysis_prompt")
        except Exception:
            metadata = PromptMetadata(
                name="performance_analysis_prompt",
                version="1.0",
                description="Analyzes performance based strictly on evidence.",
                owner_agent=self.name,
                required_variables=["evidence", "bias_findings", "employee_metadata"],
                system_prompt_path="system/performance_analysis.txt",
                user_prompt_path="user/performance_analysis.txt"
            )
            try:
                self.prompt_registry.register(metadata)
            except Exception:
                pass # Already registered

    def _validate_before_process(self, state: ReviewState) -> None:
        if not state.evidence or not state.evidence.citations:
            raise StateValidationError("Evidence citations are missing.")
            
    def _process(self, state: ReviewState, context: ExecutionContext) -> ReviewState:
        # 1. Validation
        self._validate_before_process(state)
        state.analysis.status = "processing"
        
        start_time = time.perf_counter()
        
        # 2. Gather Context
        evidence_text = "\n".join(state.evidence.citations)
        bias_text = "\n".join([f"[{f.bias_type.name}] {f.reason}" for f in state.bias.findings]) if hasattr(state, 'bias') and state.bias.findings else "No bias detected."
        employee_meta = f"Employee ID: {state.metadata.employee_id}"
        
        # 3. Render Prompts
        sys_prompt, user_prompt = self.prompt_registry.render_prompt(
            "performance_analysis_prompt", 
            variables={
                "evidence": evidence_text, 
                "bias_findings": bias_text, 
                "employee_metadata": employee_meta
            }
        )
        
        # 4. LLM Execution (Structured JSON Output)
        req = LLMRequest(
            system_prompt=sys_prompt,
            user_prompt=user_prompt,
            response_format=PerformanceAnalysisResult,
            temperature=0.0 # Deterministic reasoning
        )
        
        res = self.llm_service.generate(req, correlation_id=context.correlation_id)
        structured_res: PerformanceAnalysisResult = res.structured_data
        
        # 5. Populate State
        state.analysis.strengths = structured_res.strengths
        state.analysis.weaknesses = structured_res.improvements
        state.analysis.competencies = structured_res.competencies
        state.analysis.overall_score = _calculate_performance_score(state, structured_res.competencies)
        state.analysis.confidence_score = structured_res.confidence
        state.analysis.reasoning = structured_res.reasoning
        state.analysis.supporting_citations = structured_res.supporting_citations
        
        # Legacy mapping just in case
        state.analysis.growth_areas = structured_res.improvements
        state.analysis.overall_rating = structured_res.overall_summary
        
        latency_ms = int((time.perf_counter() - start_time) * 1000)
        state.analysis.analysis_cost = res.cost if hasattr(res, 'cost') else 0.0
        state.analysis.analysis_latency_ms = latency_ms
        state.analysis.status = "completed"
        
        # 6. Audit & Execution Logs
        state.execution.completed_steps.append(self.name)
        state.audit.agent_logs.append(
            f"[{self.name}] Evaluated performance. Cost: "
        )
        
        return state
