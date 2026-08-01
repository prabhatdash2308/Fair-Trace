"""
ReviewGuard AI — Agent 4: Bias Detection Agent
Dual-phase: LLM linguistic bias + rule-based quantitative detection.
SLO: < 10 seconds.
"""

import json
import uuid
from datetime import datetime, timezone
from collections import Counter

import structlog

from app.ai.state.review_state import ReviewGuardState, BiasFlagState
from config import settings
from app.ai.services.llm_service import call_llm_with_fallback

logger = structlog.get_logger(__name__)

PROMPT_NAME = "bias_detection/system"
PROMPT_VERSION = "v1.0"

BIAS_DETECTION_SYSTEM = """You are an expert performance review bias analyst.
Analyze the provided review text and identify cognitive biases.

You MUST respond with ONLY valid JSON in this exact format:
{
  "flags": [
    {
      "bias_type": "HALO|HORN|LENIENCY|SEVERITY|RECENCY",
      "severity": "HIGH|MEDIUM|LOW",
      "affected_text": "exact quoted text exhibiting bias",
      "detection_reasoning": "explanation of why this is a bias"
    }
  ]
}

Bias definitions:
- HALO: Global positive framing not tied to specific behaviors ("always amazing at everything")
- HORN: Global negative framing not tied to specific behaviors ("always fails to deliver")
- LENIENCY: Systematically elevated language ("never makes mistakes", "always exceeds")
- SEVERITY: Systematically harsh language ("constantly fails", "never meets expectations")
- RECENCY: Text primarily references only very recent events, ignoring earlier review period

If no bias is detected, return: {"flags": []}
Do not fabricate. Only flag what is clearly present."""


def bias_detection_node(state: ReviewGuardState) -> dict:
    """
    Bias Detection Agent — dual-phase detection.
    Phase 1: LLM linguistic bias analysis per input.
    Phase 2: Rule-based quantitative checks (recency, imbalance).
    """
    agent_name = "bias_detection_agent"
    start_time = datetime.now(timezone.utc)
    logger.info("agent_started", agent=agent_name, correlation_id=state["correlation_id"])

    try:
        all_flags: list[BiasFlagState] = []
        total_tokens = 0
        total_cost = 0.0
        model_used = settings.openai_llm_model

        # ── Phase 1: LLM Linguistic Bias Detection ─────────────────────────────
        for validated_input in state["validated_inputs"]:
            if validated_input["is_anonymized"]:
                continue  # Skip anonymized inputs for bias analysis (privacy)

            messages = [
                {"role": "system", "content": BIAS_DETECTION_SYSTEM},
                {
                    "role": "user",
                    "content": (
                        f"Input Type: {validated_input['input_type']}\n\n"
                        f"Review Text:\n{validated_input['content_text'][:3000]}"
                    ),
                },
            ]

            try:
                response_text, model_used, usage = call_llm_with_fallback(
                    messages=messages,
                    response_format={"type": "json_object"},
                    correlation_id=state["correlation_id"],
                )
                total_tokens += usage.get("total_tokens", 0)
                total_cost += usage.get("estimated_cost_usd", 0.0)

                parsed = json.loads(response_text)
                for flag_data in parsed.get("flags", []):
                    all_flags.append(BiasFlagState(
                        flag_id=str(uuid.uuid4()),
                        bias_type=flag_data.get("bias_type", "HALO"),
                        severity=flag_data.get("severity", "LOW"),
                        affected_text=flag_data.get("affected_text"),
                        source_input_id=validated_input["input_id"],
                        recommended_action=_generate_recommendation(flag_data.get("bias_type", "")),
                        detected_by_agent=agent_name,
                        detection_reasoning=flag_data.get("detection_reasoning", ""),
                    ))

            except Exception as llm_err:
                logger.warning("bias_llm_failed_for_input",
                               input_id=validated_input["input_id"], error=str(llm_err))

        # ── Phase 2: Quantitative Rule-Based Detection ─────────────────────────

        # Rule 1: Recency Bias (temporal)
        dist = state.get("stakeholder_distribution")
        if dist:
            weeks = [v["submission_week"] for v in state["validated_inputs"]]
            if weeks:
                max_week = max(weeks)
                recent_count = sum(1 for w in weeks if w >= max_week - 1)
                recent_pct = recent_count / len(weeks)
                if recent_pct > 0.70:
                    all_flags.append(BiasFlagState(
                        flag_id=str(uuid.uuid4()),
                        bias_type="RECENCY",
                        severity="HIGH" if recent_pct > 0.85 else "MEDIUM",
                        affected_text=None,
                        source_input_id=None,
                        recommended_action=(
                            "Review the distribution of inputs across the full review period. "
                            "Ensure earlier performance is equally considered."
                        ),
                        detected_by_agent=agent_name,
                        detection_reasoning=(
                            f"{int(recent_pct * 100)}% of inputs were submitted in the final 2 weeks "
                            f"of the review period (threshold: 70%)."
                        ),
                    ))

            # Rule 2: Stakeholder Imbalance
            if dist.get("is_imbalanced"):
                dominant = dist["dominant_source"]
                dominant_pct = max([
                    dist["self_assessment_pct"], dist["manager_note_pct"],
                    dist["peer_review_pct"], dist["project_outcome_pct"],
                    dist["goal_pct"], dist["meeting_note_pct"],
                ])
                all_flags.append(BiasFlagState(
                    flag_id=str(uuid.uuid4()),
                    bias_type="IMBALANCE",
                    severity="HIGH" if dominant_pct > 0.80 else "MEDIUM",
                    affected_text=None,
                    source_input_id=None,
                    recommended_action=(
                        f"Diversify input sources. '{dominant}' currently accounts for "
                        f"{int(dominant_pct * 100)}% of all inputs."
                    ),
                    detected_by_agent=agent_name,
                    detection_reasoning=(
                        f"Stakeholder imbalance: '{dominant}' = {int(dominant_pct * 100)}% "
                        f"of inputs (threshold: 60%)."
                    ),
                ))

        high_count = sum(1 for f in all_flags if f["severity"] == "HIGH")
        medium_count = sum(1 for f in all_flags if f["severity"] == "MEDIUM")

        end_time = datetime.now(timezone.utc)
        record = _build_record(
            agent_name, start_time, end_time, "SUCCESS",
            f"Detected {len(all_flags)} bias flags ({high_count} HIGH, {medium_count} MEDIUM).",
            items_processed=len(state["validated_inputs"]),
            model_used=model_used,
            tokens_total=total_tokens,
            cost=total_cost,
        )

        logger.info("agent_completed", agent=agent_name, flags=len(all_flags),
                    correlation_id=state["correlation_id"])

        return {
            "bias_flags": all_flags,
            "high_bias_count": high_count,
            "medium_bias_count": medium_count,
            "bias_detection_complete": True,
            "state_version": state["state_version"] + 1,
            "current_agent": agent_name,
            "pipeline_total_tokens": state.get("pipeline_total_tokens", 0) + total_tokens,
            "pipeline_total_cost_usd": round(state.get("pipeline_total_cost_usd", 0.0) + total_cost, 6),
            "agent_executions": [record],
        }

    except Exception as exc:
        logger.exception("agent_failed", agent=agent_name, error=str(exc))
        end_time = datetime.now(timezone.utc)
        record = _build_record(agent_name, start_time, end_time, "FAILURE", str(exc), error_message=str(exc))
        return {
            "bias_detection_complete": False,
            "pipeline_status": "FAILED",
            "error_state": {"agent": agent_name, "error": str(exc), "timestamp": end_time.isoformat()},
            "state_version": state["state_version"] + 1,
            "agent_executions": [record],
        }


def _generate_recommendation(bias_type: str) -> str:
    recommendations = {
        "HALO": "Look for specific, behavior-based evidence rather than global assessments.",
        "HORN": "Balance negative observations with documented specific behaviors.",
        "LENIENCY": "Replace absolute language with concrete performance data.",
        "SEVERITY": "Ensure critical observations are backed by documented incidents.",
        "RECENCY": "Review performance evidence from the full review period.",
        "IMBALANCE": "Gather input from additional stakeholder perspectives.",
        "UNSUPPORTED": "Verify this claim is supported by documented evidence.",
    }
    return recommendations.get(bias_type, "Review this observation for evidence-based support.")


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
