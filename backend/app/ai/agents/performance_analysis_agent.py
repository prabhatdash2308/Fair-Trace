"""
ReviewGuard AI — Agent 5: Performance Analysis Agent
Synthesizes evidence into dimension summaries and computes confidence score.
P4 enforcement: sets pipeline_status=HALTED if confidence=INSUFFICIENT.
SLO: < 10 seconds.
"""

import json
from datetime import datetime, timezone
from statistics import mean

import structlog

from app.ai.state.review_state import ReviewGuardState, ConfidenceResult
from config import settings
from app.ai.services.llm_service import call_llm_with_fallback

logger = structlog.get_logger(__name__)

PROMPT_NAME = "performance_analysis/system"
PROMPT_VERSION = "v1.0"

SYNTHESIS_SYSTEM = """You are an expert HR analyst synthesizing performance evidence.
Given evidence passages for a specific performance dimension, produce a factual 2-3 sentence summary.

Rules:
- Only use information present in the provided passages
- Do not introduce claims not supported by evidence
- Note contradictions between sources if present
- Professional tone, third person
- Do not use phrases like 'based on feedback' or 'according to reviews'

Respond with ONLY the summary text. No JSON wrapper."""


def performance_analysis_node(state: ReviewGuardState) -> dict:
    """
    Performance Analysis Agent Node.
    Synthesizes per-dimension evidence, computes confidence score.
    Halts pipeline if confidence is INSUFFICIENT (P4).
    """
    agent_name = "performance_analysis_agent"
    start_time = datetime.now(timezone.utc)
    logger.info("agent_started", agent=agent_name, correlation_id=state["correlation_id"])

    try:
        dimension_summaries: dict[str, str | None] = {}
        total_tokens = 0
        total_cost = 0.0
        model_used = settings.openai_llm_model

        for dimension, citations in state["evidence_by_dimension"].items():
            if not citations:
                dimension_summaries[dimension] = None
                continue

            passages = "\n\n".join([
                f"[Source: {c['source_input_type']}] {c['extracted_passage']}"
                for c in sorted(citations, key=lambda x: -x["similarity_score"])[:5]
            ])

            messages = [
                {"role": "system", "content": SYNTHESIS_SYSTEM},
                {
                    "role": "user",
                    "content": (
                        f"Performance Dimension: {dimension}\n\n"
                        f"Evidence Passages:\n{passages}"
                    ),
                },
            ]

            try:
                summary_text, model_used, usage = call_llm_with_fallback(
                    messages=messages,
                    correlation_id=state["correlation_id"],
                )
                total_tokens += usage.get("total_tokens", 0)
                total_cost += usage.get("estimated_cost_usd", 0.0)
                dimension_summaries[dimension] = summary_text.strip()
            except Exception as llm_err:
                logger.warning("synthesis_failed_for_dimension", dimension=dimension, error=str(llm_err))
                dimension_summaries[dimension] = None

        # ── Confidence Calculation ──────────────────────────────────────────────
        confidence = _calculate_confidence(state)

        end_time = datetime.now(timezone.utc)
        record = _build_record(
            agent_name, start_time, end_time, "SUCCESS",
            f"Synthesized {sum(1 for v in dimension_summaries.values() if v)} dimensions. "
            f"Confidence: {confidence['score']} ({confidence['numeric_score']:.0%}).",
            items_processed=len(dimension_summaries),
            model_used=model_used,
            tokens_total=total_tokens,
            cost=total_cost,
        )

        result = {
            "dimension_summaries": dimension_summaries,
            "confidence_result": confidence,
            "analysis_complete": True,
            "state_version": state["state_version"] + 1,
            "current_agent": agent_name,
            "pipeline_total_tokens": state.get("pipeline_total_tokens", 0) + total_tokens,
            "pipeline_total_cost_usd": round(state.get("pipeline_total_cost_usd", 0.0) + total_cost, 6),
            "agent_executions": [record],
        }

        # P4: Halt if insufficient confidence
        if confidence["score"] == "INSUFFICIENT":
            low_dims = state.get("low_evidence_dimensions", [])
            result["pipeline_status"] = "HALTED"
            result["error_state"] = {
                "agent": agent_name,
                "error": "INSUFFICIENT_CONFIDENCE",
                "message": (
                    f"Insufficient evidence to generate a reliable report. "
                    f"Confidence score: {confidence['numeric_score']:.0%}. "
                    f"Low-evidence dimensions: {', '.join(low_dims) if low_dims else 'multiple'}. "
                    "Please add more substantive inputs and re-trigger the pipeline."
                ),
                "timestamp": end_time.isoformat(),
            }

        logger.info("agent_completed", agent=agent_name,
                    confidence=confidence["score"], correlation_id=state["correlation_id"])
        return result

    except Exception as exc:
        logger.exception("agent_failed", agent=agent_name, error=str(exc))
        end_time = datetime.now(timezone.utc)
        record = _build_record(agent_name, start_time, end_time, "FAILURE", str(exc), error_message=str(exc))
        return {
            "analysis_complete": False,
            "pipeline_status": "FAILED",
            "error_state": {"agent": agent_name, "error": str(exc), "timestamp": end_time.isoformat()},
            "state_version": state["state_version"] + 1,
            "agent_executions": [record],
        }


def _calculate_confidence(state: ReviewGuardState) -> ConfidenceResult:
    """Deterministic confidence formula — no LLM. See Part 3 Section 7."""
    evidence = state.get("evidence_index", [])
    validated = state.get("validated_inputs", [])
    high_count = state.get("high_bias_count", 0)
    medium_count = state.get("medium_bias_count", 0)

    # Step 1: Evidence Quantity
    eq_score = min(len(evidence) / 5.0, 1.0)

    # Step 2: Evidence Quality (average cosine similarity)
    sims = [c["similarity_score"] for c in evidence]
    ql_score = mean(sims) if sims else 0.0

    # Step 3: Bias Penalty
    penalty = min(high_count * 0.15 + medium_count * 0.07, 1.0)
    bias_score = max(1.0 - penalty, 0.0)

    # Step 4: Stakeholder Coverage
    unique_types = len({v["input_type"] for v in validated})
    coverage_score = unique_types / 6.0

    # Step 5: Weighted composite
    numeric = round(
        eq_score * 0.30 + ql_score * 0.40 + bias_score * 0.20 + coverage_score * 0.10, 4
    )

    if numeric >= 0.75:
        score = "HIGH"
    elif numeric >= 0.50:
        score = "MEDIUM"
    elif numeric >= 0.30:
        score = "LOW"
    else:
        score = "INSUFFICIENT"

    explanation = (
        f"Confidence rated {score} ({numeric:.0%}). "
        f"Evidence: {len(evidence)} citation(s) found (avg similarity: {ql_score:.0%}). "
        f"Bias: {high_count} HIGH + {medium_count} MEDIUM flags. "
        f"Input sources: {unique_types} of 6 types provided."
    )

    return ConfidenceResult(
        score=score,
        numeric_score=numeric,
        evidence_quantity_score=eq_score,
        evidence_quality_score=ql_score,
        bias_flag_penalty=penalty,
        stakeholder_coverage_score=coverage_score,
        explanation=explanation,
    )


def _build_record(agent_name, start, end, status, summary, error_message=None,
                  items_processed=0, model_used=None, tokens_total=0, cost=0.0):
    return {
        "agent_name": agent_name,
        "start_time": start.isoformat(),
        "end_time": end.isoformat(),
        "status": status,
        "output_summary": summary,
        "error_message": error_message,
        "items_processed": items_processed,
        "llm_model_used": model_used,
        "tokens_prompt": None, "tokens_completion": None,
        "tokens_total": tokens_total,
        "estimated_cost_usd": cost,
        "latency_ms": int((end - start).total_seconds() * 1000),
        "prompt_name": PROMPT_NAME,
        "prompt_version": PROMPT_VERSION,
        "correlation_id": None, "llm_request_id": None,
    }
