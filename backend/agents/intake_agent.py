"""
ReviewGuard AI — Agent 1: Intake Agent
Validates and normalizes all review inputs for a cycle.
No LLM calls — pure Python data validation and stakeholder analysis.
SLO: < 1 second
"""

from datetime import datetime, timezone

import structlog

from agents.state import ReviewGuardState, ValidatedInput, StakeholderDistribution
from models.enums import InputType
from repositories import review_input_repo
from core.database import SessionLocal

logger = structlog.get_logger(__name__)

MINIMUM_CHAR_COUNT = 50
LOW_CHAR_WARNING_THRESHOLD = 200
IMBALANCE_THRESHOLD = 0.60


def intake_agent_node(state: ReviewGuardState) -> dict:
    """
    Intake Agent Node — Entry point of the pipeline.
    Fetches inputs, validates structure, computes stakeholder distribution.
    """
    agent_name = "intake_agent"
    start_time = datetime.now(timezone.utc)
    logger.info("agent_started", agent=agent_name, correlation_id=state["correlation_id"])

    db = SessionLocal()
    try:
        cycle_id = state["review_cycle_id"]
        inputs = review_input_repo.list_for_cycle(db, cycle_id)  # type: ignore[arg-type]

        if not inputs:
            return _fail(state, agent_name, start_time, "No inputs submitted for this review cycle.")

        # ── Build ValidatedInput list ───────────────────────────────────────────
        validated: list[ValidatedInput] = []
        warnings: list[str] = []

        for inp in inputs:
            text = inp.content_text.strip()
            if len(text) < MINIMUM_CHAR_COUNT:
                warnings.append(
                    f"Input {inp.id} ({inp.input_type.value}) has fewer than {MINIMUM_CHAR_COUNT} characters — skipped."
                )
                continue
            if len(text) < LOW_CHAR_WARNING_THRESHOLD:
                warnings.append(
                    f"Input {inp.id} ({inp.input_type.value}) has low character count ({len(text)} chars)."
                )

            submitted_at = inp.submitted_at or datetime.now(timezone.utc)
            validated.append(ValidatedInput(
                input_id=str(inp.id),
                input_type=inp.input_type.value,
                content_text=text,
                submitted_by_id=str(inp.submitted_by),
                submitted_at=submitted_at.isoformat(),
                is_anonymized=inp.is_anonymized,
                char_count=len(text),
                submission_week=submitted_at.isocalendar().week,
            ))

        if not validated:
            return _fail(state, agent_name, start_time, "All inputs were below the minimum character threshold.")

        # ── Validate minimum source requirements ────────────────────────────────
        types_present = {v["input_type"] for v in validated}
        if InputType.SELF_ASSESSMENT.value not in types_present:
            return _fail(state, agent_name, start_time,
                         "A self-assessment is required to proceed with the pipeline.")
        if len(types_present) < 2:
            return _fail(state, agent_name, start_time,
                         "At least two different input source types are required.")

        # ── Stakeholder Distribution ────────────────────────────────────────────
        total = len(validated)
        counts: dict[str, int] = {t.value: 0 for t in InputType}
        for v in validated:
            counts[v["input_type"]] = counts.get(v["input_type"], 0) + 1

        distribution = StakeholderDistribution(
            self_assessment_pct=round(counts.get("SELF_ASSESSMENT", 0) / total, 3),
            manager_note_pct=round(counts.get("MANAGER_NOTE", 0) / total, 3),
            peer_review_pct=round(counts.get("PEER_REVIEW", 0) / total, 3),
            project_outcome_pct=round(counts.get("PROJECT_OUTCOME", 0) / total, 3),
            goal_pct=round(counts.get("GOAL", 0) / total, 3),
            meeting_note_pct=round(counts.get("MEETING_NOTE", 0) / total, 3),
            dominant_source=max(counts, key=counts.get),  # type: ignore
            is_imbalanced=any(c / total > IMBALANCE_THRESHOLD for c in counts.values()),
        )

        if distribution["is_imbalanced"]:
            warnings.append(
                f"Stakeholder imbalance detected: '{distribution['dominant_source']}' "
                f"contributes > {int(IMBALANCE_THRESHOLD * 100)}% of all inputs."
            )

        end_time = datetime.now(timezone.utc)
        execution_record = _build_record(
            agent_name, start_time, end_time, "SUCCESS",
            f"Validated {len(validated)} inputs across {len(types_present)} source types.",
            items_processed=len(validated),
        )

        logger.info("agent_completed", agent=agent_name, items=len(validated),
                    correlation_id=state["correlation_id"])

        return {
            "validated_inputs": validated,
            "intake_complete": True,
            "intake_warnings": warnings,
            "stakeholder_distribution": distribution,
            "state_version": state["state_version"] + 1,
            "current_agent": agent_name,
            "agent_executions": [execution_record],
        }

    except Exception as exc:
        logger.exception("agent_failed", agent=agent_name, error=str(exc))
        return _fail(state, agent_name, start_time, str(exc))
    finally:
        db.close()


def _fail(state: ReviewGuardState, agent: str, start: datetime, message: str) -> dict:
    end_time = datetime.now(timezone.utc)
    record = _build_record(agent, start, end_time, "FAILURE", message, error_message=message)
    return {
        "intake_complete": False,
        "pipeline_status": "FAILED",
        "error_state": {"agent": agent, "error": message, "timestamp": end_time.isoformat()},
        "state_version": state["state_version"] + 1,
        "agent_executions": [record],
    }


def _build_record(
    agent_name: str,
    start: datetime,
    end: datetime,
    status: str,
    summary: str,
    error_message: str | None = None,
    items_processed: int = 0,
) -> dict:
    return {
        "agent_name": agent_name,
        "start_time": start.isoformat(),
        "end_time": end.isoformat(),
        "status": status,
        "output_summary": summary,
        "error_message": error_message,
        "items_processed": items_processed,
        "llm_model_used": None,
        "tokens_prompt": None,
        "tokens_completion": None,
        "tokens_total": None,
        "estimated_cost_usd": None,
        "latency_ms": int((end - start).total_seconds() * 1000),
        "prompt_name": None,
        "prompt_version": None,
        "correlation_id": None,
        "llm_request_id": None,
    }
