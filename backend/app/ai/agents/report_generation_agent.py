"""
ReviewGuard AI — Agent 6: Report Generation Agent
Generates performance claims, executive summary, and recommendations.
Persists entire report to PostgreSQL in a single transaction.
P1: No claim generated without at least 1 supporting citation.
SLO: < 8 seconds.
"""

import json
import uuid
from datetime import datetime, timezone

import structlog

from app.ai.state.review_state import ReviewGuardState, PerformanceClaimState, EvidenceCitationState
from config import settings
from core.database import SessionLocal
from app.ai.services.llm_service import call_llm_with_fallback
from models.enums import ConfidenceLevel, ReportStatus
from repositories import audit_repo, report_repo, bias_flag_repo, citation_repo
from repositories.repositories import report_repo as rrepo
from models.enums import AuditEventType

logger = structlog.get_logger(__name__)

PROMPT_NAME = "report_generation/system"
PROMPT_VERSION = "v1.0"

CLAIM_SYSTEM = """You are an expert HR analyst generating performance review claims.
Given evidence passages, generate exactly ONE performance claim for the dimension.

Rules:
- The claim MUST be directly supported by the provided evidence
- 1-2 sentences, professional tone, third person
- Do not reference "feedback", "reviews", or "according to"
- Do not fabricate information not in the evidence

Respond with ONLY the claim text. No JSON, no explanation."""

SUMMARY_SYSTEM = """You are an expert HR analyst.
Given performance claims across dimensions, write a 3-5 sentence executive summary.
Professional tone. Evidence-grounded. Balanced. No new information beyond the claims.
Respond with ONLY the summary text."""

ACTIONS_SYSTEM = """You are an expert HR analyst.
Given bias flags and dimension summaries, generate exactly 3 actionable recommendations.
Each must reference a specific finding. Concrete and measurable.

Respond with ONLY a JSON array of 3 strings:
["recommendation 1", "recommendation 2", "recommendation 3"]"""


def report_generation_node(state: ReviewGuardState) -> dict:
    """
    Report Generation Agent Node.
    Generates claims per dimension, executive summary, recommendations.
    Persists everything to PostgreSQL atomically.
    """
    agent_name = "report_generation_agent"
    start_time = datetime.now(timezone.utc)
    logger.info("agent_started", agent=agent_name, correlation_id=state["correlation_id"])

    db = SessionLocal()
    try:
        claims: list[PerformanceClaimState] = []
        final_citations: list[EvidenceCitationState] = []
        total_tokens = 0
        total_cost = 0.0
        model_used = settings.openai_llm_model

        # ── Generate Claims Per Dimension ──────────────────────────────────────
        for order_idx, (dimension, summary) in enumerate(state["dimension_summaries"].items()):
            if not summary:
                continue

            dim_citations = state["evidence_by_dimension"].get(dimension, [])
            if not dim_citations:
                # P1: no citation → no claim → unsupported flag instead
                logger.info("no_citation_skipping_dimension", dimension=dimension)
                continue

            top_citations = sorted(dim_citations, key=lambda c: -c["similarity_score"])[:3]
            passages = "\n\n".join([
                f"[{c['source_input_type']}]: {c['extracted_passage']}"
                for c in top_citations
            ])

            messages = [
                {"role": "system", "content": CLAIM_SYSTEM},
                {
                    "role": "user",
                    "content": (
                        f"Dimension: {dimension}\n\n"
                        f"Analysis Summary: {summary}\n\n"
                        f"Supporting Evidence:\n{passages}"
                    ),
                },
            ]

            try:
                claim_text, model_used, usage = call_llm_with_fallback(
                    messages=messages, correlation_id=state["correlation_id"]
                )
                total_tokens += usage.get("total_tokens", 0)
                total_cost += usage.get("estimated_cost_usd", 0.0)

                conf = state["confidence_result"]
                numeric = conf["numeric_score"] if conf else 0
                claim_confidence = (
                    "HIGH" if numeric >= 0.75 else "MEDIUM" if numeric >= 0.50 else "LOW"
                )

                claim_id = str(uuid.uuid4())
                citation_ids = [c["citation_id"] for c in top_citations]

                claims.append(PerformanceClaimState(
                    claim_id=claim_id,
                    dimension=dimension,
                    claim_text=claim_text.strip(),
                    explanation="",  # Filled by Explainability Agent
                    confidence=claim_confidence,
                    evidence_citation_ids=citation_ids,
                    is_supported=True,
                    display_order=order_idx,
                ))
                final_citations.extend(top_citations)

            except Exception as llm_err:
                logger.warning("claim_generation_failed", dimension=dimension, error=str(llm_err))

        if not claims:
            return _fail(state, agent_name, start_time, db,
                         "No claims could be generated — all dimensions lacked sufficient evidence.")

        # ── Executive Summary ──────────────────────────────────────────────────
        claim_texts = "\n".join([f"- [{c['dimension']}]: {c['claim_text']}" for c in claims])
        exec_messages = [
            {"role": "system", "content": SUMMARY_SYSTEM},
            {"role": "user", "content": f"Performance Claims:\n{claim_texts}"},
        ]
        exec_summary, _, exec_usage = call_llm_with_fallback(
            messages=exec_messages, correlation_id=state["correlation_id"]
        )
        total_tokens += exec_usage.get("total_tokens", 0)
        total_cost += exec_usage.get("estimated_cost_usd", 0.0)

        # ── Recommended Actions ────────────────────────────────────────────────
        bias_summary = "\n".join([
            f"- {f['bias_type']} ({f['severity']}): {f['detection_reasoning']}"
            for f in state["bias_flags"][:5]
        ])
        dim_summary = "\n".join([
            f"- {dim}: {summ[:200]}"
            for dim, summ in state["dimension_summaries"].items() if summ
        ])
        actions_messages = [
            {"role": "system", "content": ACTIONS_SYSTEM},
            {
                "role": "user",
                "content": (
                    f"Bias Flags:\n{bias_summary or 'None detected.'}\n\n"
                    f"Dimension Summaries:\n{dim_summary}"
                ),
            },
        ]
        actions_text, _, actions_usage = call_llm_with_fallback(
            messages=actions_messages,
            response_format={"type": "json_object"},
            correlation_id=state["correlation_id"],
        )
        total_tokens += actions_usage.get("total_tokens", 0)
        total_cost += actions_usage.get("estimated_cost_usd", 0.0)

        try:
            recommended_actions = json.loads(actions_text)
            if not isinstance(recommended_actions, list):
                recommended_actions = [str(recommended_actions)]
        except Exception:
            recommended_actions = [actions_text]

        # ── Persist to PostgreSQL (single transaction) ─────────────────────────
        conf = state.get("confidence_result")
        report = report_repo.create(db, {
            "review_cycle_id": state["review_cycle_id"],
            "version": state.get("report_version", 1),
            "status": ReportStatus.DRAFT,
            "executive_summary": exec_summary.strip(),
            "recommended_actions": recommended_actions,
            "confidence_score": conf["score"] if conf else None,
            "confidence_explanation": conf["explanation"] if conf else None,
            "pipeline_run_id": state["pipeline_run_id"],
            "is_current": True,
        })

        # Persist claims and citations
        for claim_state in claims:
            dim_citations = [
                c for c in final_citations
                if c["citation_id"] in claim_state["evidence_citation_ids"]
            ]
            claim_record = db.execute(
                __import__("sqlalchemy").text(
                    "INSERT INTO performance_claims "
                    "(id, report_id, dimension, claim_text, explanation, confidence, is_supported, display_order, created_at, updated_at) "
                    "VALUES (:id, :report_id, :dimension, :claim_text, :explanation, :confidence, :is_supported, :display_order, now(), now()) "
                    "RETURNING id"
                ),
                {
                    "id": claim_state["claim_id"],
                    "report_id": str(report.id),
                    "dimension": claim_state["dimension"],
                    "claim_text": claim_state["claim_text"],
                    "explanation": "",
                    "confidence": claim_state["confidence"],
                    "is_supported": claim_state["is_supported"],
                    "display_order": claim_state["display_order"],
                },
            )

            for cit in dim_citations:
                citation_repo.create(db, {
                    "claim_id": claim_state["claim_id"],
                    "review_input_id": cit["source_input_id"],
                    "extracted_passage": cit["extracted_passage"],
                    "similarity_score": cit["similarity_score"],
                    "retrieval_rank": cit["retrieval_rank"],
                })

        # Persist bias flags
        for flag in state["bias_flags"]:
            bias_flag_repo.create(db, {
                "report_id": str(report.id),
                "review_input_id": flag.get("source_input_id"),
                "bias_type": flag["bias_type"],
                "severity": flag["severity"],
                "affected_text": flag.get("affected_text"),
                "recommended_action": flag["recommended_action"],
                "detected_by_agent": flag["detected_by_agent"],
                "detection_reasoning": flag["detection_reasoning"],
            })

        audit_repo.create(db, {
            "event_type": AuditEventType.REPORT_GENERATED,
            "actor_id": None,
            "resource_type": "report",
            "resource_id": report.id,
            "event_payload": {
                "pipeline_run_id": state["pipeline_run_id"],
                "claims_count": len(claims),
                "confidence": conf["score"] if conf else "UNKNOWN",
            },
            "correlation_id": state["pipeline_run_id"],
            "state_version": state["state_version"] + 1,
        })

        db.commit()

        end_time = datetime.now(timezone.utc)
        record = _build_record(
            agent_name, start_time, end_time, "SUCCESS",
            f"Generated {len(claims)} claims, executive summary, and 3 recommended actions.",
            items_processed=len(claims),
            model_used=model_used,
            tokens_total=total_tokens,
            cost=total_cost,
        )

        logger.info("agent_completed", agent=agent_name, claims=len(claims),
                    report_id=str(report.id), correlation_id=state["correlation_id"])

        return {
            "performance_claims": claims,
            "evidence_citations": final_citations,
            "executive_summary": exec_summary.strip(),
            "recommended_actions": recommended_actions,
            "report_db_id": str(report.id),
            "report_version": state.get("report_version", 1),
            "report_complete": True,
            "state_version": state["state_version"] + 1,
            "current_agent": agent_name,
            "pipeline_total_tokens": state.get("pipeline_total_tokens", 0) + total_tokens,
            "pipeline_total_cost_usd": round(state.get("pipeline_total_cost_usd", 0.0) + total_cost, 6),
            "agent_executions": [record],
        }

    except Exception as exc:
        db.rollback()
        logger.exception("agent_failed", agent=agent_name, error=str(exc))
        return _fail(state, agent_name, start_time, db, str(exc))
    finally:
        db.close()


def _fail(state, agent_name, start_time, db, message):
    end_time = datetime.now(timezone.utc)
    record = _build_record(agent_name, start_time, end_time, "FAILURE", message, error_message=message)
    return {
        "report_complete": False,
        "pipeline_status": "FAILED",
        "error_state": {"agent": agent_name, "error": message, "timestamp": end_time.isoformat()},
        "state_version": state["state_version"] + 1,
        "agent_executions": [record],
    }


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
