"""
ReviewGuard AI — Agent 3: Evidence Retrieval Agent
Performs semantic search for all 5 performance dimensions.
P1 gate: sets evidence_ready=False if no evidence found. SLO: < 3 seconds.
"""

import uuid
from datetime import datetime, timezone

import structlog

from app.ai.state.review_state import ReviewGuardState, EvidenceCitationState
from config import settings
from app.ai.services.llm_service import embed_single
from app.ai.services.qdrant_service import search_by_cycle

logger = structlog.get_logger(__name__)

# Canonical dimension queries — do not modify without PR review
DIMENSION_QUERIES: dict[str, list[str]] = {
    "TECHNICAL": [
        "technical skills code quality engineering system design technical delivery software development"
    ],
    "COLLABORATION": [
        "collaboration teamwork communication cross-functional helping others knowledge sharing"
    ],
    "LEADERSHIP": [
        "leadership mentoring decision making initiative ownership driving outcomes"
    ],
    "DELIVERY": [
        "delivery deadlines project completion results execution on-time delivery milestones"
    ],
    "GROWTH": [
        "learning growth improvement feedback development new skills professional development"
    ],
}


def evidence_retrieval_node(state: ReviewGuardState) -> dict:
    """
    Evidence Retrieval Agent Node.
    Queries Qdrant for each dimension and builds the evidence index.
    Sets evidence_ready=False if no passages retrieved above threshold (P1 enforcement).
    """
    agent_name = "evidence_retrieval_agent"
    start_time = datetime.now(timezone.utc)
    logger.info("agent_started", agent=agent_name, correlation_id=state["correlation_id"])

    try:
        evidence_index: list[EvidenceCitationState] = []
        evidence_by_dimension: dict[str, list[EvidenceCitationState]] = {}
        low_evidence_dimensions: list[str] = []

        for dimension, queries in DIMENSION_QUERIES.items():
            dimension_citations: list[EvidenceCitationState] = []

            for query_text in queries:
                query_vector = embed_single(query_text)
                results = search_by_cycle(
                    query_vector=query_vector,
                    review_cycle_id=state["review_cycle_id"],
                    top_k=settings.max_evidence_chunks,
                    score_threshold=settings.similarity_threshold,
                )

                for rank, result in enumerate(results):
                    citation = EvidenceCitationState(
                        citation_id=str(uuid.uuid4()),
                        source_input_id=result["payload"].get("review_input_id", ""),
                        source_input_type=result["payload"].get("input_type", ""),
                        extracted_passage=result["payload"].get("chunk_text", ""),
                        similarity_score=round(result["score"], 4),
                        retrieval_rank=rank + 1,
                        query_dimension=dimension,
                    )
                    dimension_citations.append(citation)

            if len(dimension_citations) < 2:
                low_evidence_dimensions.append(dimension)

            evidence_by_dimension[dimension] = dimension_citations
            evidence_index.extend(dimension_citations)

        evidence_ready = len(evidence_index) > 0

        end_time = datetime.now(timezone.utc)
        record = _build_record(
            agent_name, start_time, end_time,
            "SUCCESS" if evidence_ready else "FAILURE",
            f"Retrieved {len(evidence_index)} citations across {len(DIMENSION_QUERIES)} dimensions.",
            error_message=None if evidence_ready else "No evidence retrieved above similarity threshold.",
            items_processed=len(evidence_index),
        )

        logger.info(
            "agent_completed", agent=agent_name,
            citations=len(evidence_index), evidence_ready=evidence_ready,
            correlation_id=state["correlation_id"],
        )

        result = {
            "evidence_index": evidence_index,
            "evidence_by_dimension": evidence_by_dimension,
            "evidence_ready": evidence_ready,
            "low_evidence_dimensions": low_evidence_dimensions,
            "state_version": state["state_version"] + 1,
            "current_agent": agent_name,
            "agent_executions": [record],
        }

        if not evidence_ready:
            result["pipeline_status"] = "FAILED"
            result["error_state"] = {
                "agent": agent_name,
                "error": "No evidence retrieved above similarity threshold 0.60.",
                "timestamp": end_time.isoformat(),
            }

        return result

    except Exception as exc:
        logger.exception("agent_failed", agent=agent_name, error=str(exc))
        end_time = datetime.now(timezone.utc)
        record = _build_record(agent_name, start_time, end_time, "FAILURE", str(exc), error_message=str(exc))
        return {
            "evidence_ready": False,
            "pipeline_status": "FAILED",
            "error_state": {"agent": agent_name, "error": str(exc), "timestamp": end_time.isoformat()},
            "state_version": state["state_version"] + 1,
            "agent_executions": [record],
        }


def _build_record(agent_name, start, end, status, summary, error_message=None, items_processed=0):
    return {
        "agent_name": agent_name,
        "start_time": start.isoformat(),
        "end_time": end.isoformat(),
        "status": status,
        "output_summary": summary,
        "error_message": error_message,
        "items_processed": items_processed,
        "llm_model_used": settings.openai_embedding_model,
        "tokens_prompt": None, "tokens_completion": None, "tokens_total": None,
        "estimated_cost_usd": None,
        "latency_ms": int((end - start).total_seconds() * 1000),
        "prompt_name": None, "prompt_version": None,
        "correlation_id": None, "llm_request_id": None,
    }
