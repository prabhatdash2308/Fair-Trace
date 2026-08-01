"""
ReviewGuard AI — Agent 7: Explainability Agent
Builds 5-step ExplanationTrace for every claim.
Computes evaluation metrics for the Report Quality Dashboard.
SLO: < 8 seconds.
"""

from datetime import datetime, timezone
from statistics import mean
from uuid import UUID

import structlog

from agents.state import ReviewGuardState, ExplanationTrace
from config import settings
from core.database import SessionLocal
from core.llm import call_llm_with_fallback
from sqlalchemy import text

logger = structlog.get_logger(__name__)

PROMPT_NAME = "explainability/synthesis"
PROMPT_VERSION = "v1.0"

SYNTHESIS_SYSTEM = """You are an expert at explaining AI reasoning.
In exactly ONE sentence, explain how the provided evidence passages support the given performance claim.
Reference the actual content of the passages — be specific, not generic.
Respond with ONLY the sentence."""


def explainability_node(state: ReviewGuardState) -> dict:
    """
    Explainability Agent Node.
    Steps 1, 2, 4, 5 are deterministic. Step 3 uses GPT-4o.
    Updates claim explanations in PostgreSQL.
    """
    agent_name = "explainability_agent"
    start_time = datetime.now(timezone.utc)
    logger.info("agent_started", agent=agent_name, correlation_id=state["correlation_id"])

    db = SessionLocal()
    try:
        traces: list[ExplanationTrace] = []
        total_tokens = 0
        total_cost = 0.0
        model_used = settings.openai_llm_model

        for claim in state["performance_claims"]:
            # Citations supporting this claim
            supporting_cits = [
                c for c in state["evidence_citations"]
                if c["citation_id"] in claim["evidence_citation_ids"]
            ]
            # Bias flags on those citations' source inputs
            source_input_ids = {c["source_input_id"] for c in supporting_cits}
            bias_on_evidence = [
                f for f in state["bias_flags"]
                if f.get("source_input_id") in source_input_ids
            ]
            unique_source_types = {c["source_input_type"] for c in supporting_cits}
            sims = [c["similarity_score"] for c in supporting_cits]
            avg_sim = mean(sims) if sims else 0.0

            # Step 1 — deterministic
            step1 = (
                f"Found {len(supporting_cits)} evidence passage(s) from "
                f"{len(unique_source_types)} source type(s) for dimension {claim['dimension']} "
                f"(similarity range: {min(sims):.0%}–{max(sims):.0%})."
                if sims else
                f"Found {len(supporting_cits)} evidence passage(s) for dimension {claim['dimension']}."
            )

            # Step 2 — deterministic
            quality_label = "High" if avg_sim > 0.75 else "Moderate" if avg_sim > 0.60 else "Low"
            step2 = (
                f"Average evidence relevance: {avg_sim:.0%} — {quality_label} confidence "
                f"in the match between evidence and this dimension."
            )

            # Step 3 — GPT-4o synthesis
            passages_text = "\n".join([
                f"[{c['source_input_type']}]: {c['extracted_passage'][:300]}"
                for c in supporting_cits
            ])
            try:
                synth_messages = [
                    {"role": "system", "content": SYNTHESIS_SYSTEM},
                    {
                        "role": "user",
                        "content": (
                            f"Claim: {claim['claim_text']}\n\n"
                            f"Evidence Passages:\n{passages_text}"
                        ),
                    },
                ]
                step3_text, model_used, usage = call_llm_with_fallback(
                    messages=synth_messages, correlation_id=state["correlation_id"]
                )
                total_tokens += usage.get("total_tokens", 0)
                total_cost += usage.get("estimated_cost_usd", 0.0)
                step3 = step3_text.strip()
            except Exception:
                step3 = "Evidence passages collectively support this dimension assessment."

            # Step 4 — deterministic
            if bias_on_evidence:
                sev_summary = ", ".join(
                    f"{f['bias_type']} ({f['severity']})" for f in bias_on_evidence[:3]
                )
                step4 = (
                    f"{len(bias_on_evidence)} bias flag(s) detected on supporting evidence: {sev_summary}. "
                    "Consider reviewing the flagged passages."
                )
            else:
                step4 = "No bias flags detected on the supporting evidence passages."

            # Step 5 — deterministic
            multi_source = len(unique_source_types) > 1
            step5 = (
                f"Confidence: {claim['confidence']}. Claim is "
                + ("supported by multi-source evidence." if multi_source
                   else "supported by single-source evidence — verify against other inputs.")
            )

            trace = ExplanationTrace(
                claim_id=claim["claim_id"],
                step_1_evidence_found=step1,
                step_2_evidence_quality=step2,
                step_3_synthesis=step3,
                step_4_bias_check=step4,
                step_5_conclusion=step5,
            )
            traces.append(trace)

            # Update explanation in PostgreSQL
            full_explanation = f"{step1} {step2} {step3} {step4} {step5}"
            db.execute(
                text(
                    "UPDATE performance_claims SET explanation = :explanation "
                    "WHERE id = :claim_id"
                ),
                {"explanation": full_explanation, "claim_id": claim["claim_id"]},
            )

        # ── Evaluation Metrics ─────────────────────────────────────────────────
        all_claims = state["performance_claims"]
        total_claims = len(all_claims)
        supported = sum(1 for c in all_claims if c["is_supported"])
        all_sims = [c["similarity_score"] for c in state["evidence_citations"]]
        dist = state.get("stakeholder_distribution") or {}

        source_pcts = [
            dist.get("self_assessment_pct", 0),
            dist.get("manager_note_pct", 0),
            dist.get("peer_review_pct", 0),
            dist.get("project_outcome_pct", 0),
            dist.get("goal_pct", 0),
            dist.get("meeting_note_pct", 0),
        ]

        evaluation_metrics = {
            "evidence_coverage_rate": (supported / total_claims * 100) if total_claims else 0,
            "average_citation_quality": round(mean(all_sims), 4) if all_sims else 0,
            "unsupported_claim_rate": ((total_claims - supported) / total_claims * 100) if total_claims else 0,
            "bias_flag_density": (
                len(state["bias_flags"]) / len(state["validated_inputs"])
                if state["validated_inputs"] else 0
            ),
            "dimension_coverage": (
                sum(1 for c in all_claims if c["is_supported"]) / 5 * 100
            ),
            "stakeholder_balance_score": round(1 - max(source_pcts), 3) if source_pcts else 0,
        }

        db.commit()

        end_time = datetime.now(timezone.utc)
        record = _build_record(
            agent_name, start_time, end_time, "SUCCESS",
            f"Generated {len(traces)} explanation traces. Evidence coverage: {evaluation_metrics['evidence_coverage_rate']:.0f}%.",
            items_processed=len(traces),
            model_used=model_used,
            tokens_total=total_tokens,
            cost=total_cost,
        )

        logger.info("agent_completed", agent=agent_name, traces=len(traces),
                    correlation_id=state["correlation_id"])

        return {
            "explanation_traces": traces,
            "evaluation_metrics": evaluation_metrics,
            "explainability_complete": True,
            "state_version": state["state_version"] + 1,
            "current_agent": agent_name,
            "pipeline_total_tokens": state.get("pipeline_total_tokens", 0) + total_tokens,
            "pipeline_total_cost_usd": round(state.get("pipeline_total_cost_usd", 0.0) + total_cost, 6),
            "agent_executions": [record],
        }

    except Exception as exc:
        db.rollback()
        logger.exception("agent_failed", agent=agent_name, error=str(exc))
        end_time = datetime.now(timezone.utc)
        record = _build_record(agent_name, start_time, end_time, "FAILURE", str(exc), error_message=str(exc))
        return {
            "explainability_complete": False,
            "pipeline_status": "FAILED",
            "error_state": {"agent": agent_name, "error": str(exc), "timestamp": end_time.isoformat()},
            "state_version": state["state_version"] + 1,
            "agent_executions": [record],
        }
    finally:
        db.close()


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
