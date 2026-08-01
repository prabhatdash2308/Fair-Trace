"""
ReviewGuard AI — Agent 2: Embedding Agent
Chunks all validated inputs and upserts embeddings into the single Qdrant collection.
Uses text-embedding-3-small. SLO: < 8 seconds.
"""

import uuid
from datetime import datetime, timezone

import structlog
from qdrant_client.models import PointStruct

from agents.state import ReviewGuardState
from config import settings
from core.llm import embed_texts
from core.vector_store import COLLECTION_NAME, ensure_collection, upsert_points
from repositories import review_input_repo
from core.database import SessionLocal

logger = structlog.get_logger(__name__)


def embedding_agent_node(state: ReviewGuardState) -> dict:
    """
    Embedding Agent Node.
    Chunks validated inputs, generates embeddings, upserts to Qdrant.
    All documents stored in single 'reviewguard_documents' collection filtered by review_cycle_id.
    """
    agent_name = "embedding_agent"
    start_time = datetime.now(timezone.utc)
    logger.info("agent_started", agent=agent_name, correlation_id=state["correlation_id"])

    db = SessionLocal()
    try:
        ensure_collection()

        all_points: list[PointStruct] = []
        embedded_ids: list[str] = []
        total_chunks = 0

        for validated_input in state["validated_inputs"]:
            chunks = _chunk_text(
                validated_input["content_text"],
                chunk_size=settings.chunk_size_chars,
                overlap=settings.chunk_overlap_chars,
            )

            texts = [chunk for chunk in chunks if chunk.strip()]
            if not texts:
                continue

            embeddings = embed_texts(texts)

            for idx, (chunk, vector) in enumerate(zip(texts, embeddings)):
                point = PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={
                        "review_input_id": validated_input["input_id"],
                        "review_cycle_id": state["review_cycle_id"],
                        "employee_id": state["employee_id"],
                        "input_type": validated_input["input_type"],
                        "submitted_by_id": validated_input["submitted_by_id"],
                        "chunk_text": chunk,
                        "chunk_index": idx,
                        "total_chunks": len(texts),
                        "submitted_at": validated_input["submitted_at"],
                        "submission_week": validated_input["submission_week"],
                        "is_anonymized": validated_input["is_anonymized"],
                    },
                )
                all_points.append(point)
                total_chunks += 1

            # Track the first chunk ID as the document reference
            first_point_id = all_points[-len(texts)].id if texts else None
            if first_point_id:
                review_input_repo.update_qdrant_id(
                    db, validated_input["input_id"], first_point_id  # type: ignore[arg-type]
                )
            embedded_ids.append(validated_input["input_id"])

        # Batch upsert all points
        if all_points:
            upsert_points(all_points)
        db.commit()

        end_time = datetime.now(timezone.utc)
        record = _build_record(
            agent_name, start_time, end_time, "SUCCESS",
            f"Embedded {len(embedded_ids)} inputs into {total_chunks} chunks.",
            items_processed=total_chunks,
        )

        logger.info("agent_completed", agent=agent_name, chunks=total_chunks,
                    correlation_id=state["correlation_id"])

        return {
            "qdrant_collection_name": COLLECTION_NAME,
            "embedded_input_ids": embedded_ids,
            "total_chunks_created": total_chunks,
            "embedding_complete": True,
            "state_version": state["state_version"] + 1,
            "current_agent": agent_name,
            "agent_executions": [record],
        }

    except Exception as exc:
        logger.exception("agent_failed", agent=agent_name, error=str(exc))
        end_time = datetime.now(timezone.utc)
        record = _build_record(agent_name, start_time, end_time, "FAILURE", str(exc), error_message=str(exc))
        return {
            "embedding_complete": False,
            "pipeline_status": "FAILED",
            "error_state": {"agent": agent_name, "error": str(exc), "timestamp": end_time.isoformat()},
            "state_version": state["state_version"] + 1,
            "agent_executions": [record],
        }
    finally:
        db.close()


def _chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split text into overlapping character-based chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
        if start >= len(text):
            break
    return [c.strip() for c in chunks if c.strip()]


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
