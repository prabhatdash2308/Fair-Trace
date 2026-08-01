"""
ReviewGuard AI — Qdrant Vector Store Client
Single collection strategy: all documents in 'reviewguard_documents'.
Filtered by review_cycle_id, employee_id, and input_type via payload filters.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    SearchRequest,
)

from config import settings

# Module-level client — initialized once
_client: QdrantClient | None = None

COLLECTION_NAME = settings.qdrant_collection_name  # "reviewguard_documents"


def get_qdrant_client() -> QdrantClient:
    """Returns the singleton Qdrant client, initializing if needed."""
    global _client
    if _client is None:
        _client = QdrantClient(url=settings.qdrant_url)
    return _client


def ensure_collection() -> None:
    """
    Ensures the single shared Qdrant collection exists.
    Called once at application startup.
    Creates collection if it does not exist; leaves it untouched if it does.
    """
    client = get_qdrant_client()
    existing = {c.name for c in client.get_collections().collections}
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=settings.embedding_dimension,
                distance=Distance.COSINE,
            ),
        )


def upsert_points(points: list[PointStruct]) -> None:
    """Upserts a batch of points into the shared collection."""
    client = get_qdrant_client()
    client.upsert(collection_name=COLLECTION_NAME, points=points)


def search_by_cycle(
    query_vector: list[float],
    review_cycle_id: str,
    top_k: int = 5,
    score_threshold: float = 0.60,
) -> list[dict]:
    """
    Semantic search scoped to a specific review cycle.
    Returns list of dicts with {id, score, payload}.
    """
    client = get_qdrant_client()
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="review_cycle_id",
                    match=MatchValue(value=review_cycle_id),
                )
            ]
        ),
        limit=top_k,
        score_threshold=score_threshold,
        with_payload=True,
    )
    return [
        {"id": str(r.id), "score": r.score, "payload": r.payload}
        for r in results
    ]


def delete_by_cycle(review_cycle_id: str) -> None:
    """Removes all points for a given review cycle (cleanup utility)."""
    client = get_qdrant_client()
    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=Filter(
            must=[
                FieldCondition(
                    key="review_cycle_id",
                    match=MatchValue(value=review_cycle_id),
                )
            ]
        ),
    )


def health_check() -> bool:
    """Returns True if Qdrant is reachable and collection exists."""
    try:
        client = get_qdrant_client()
        collections = {c.name for c in client.get_collections().collections}
        return COLLECTION_NAME in collections
    except Exception:
        return False
