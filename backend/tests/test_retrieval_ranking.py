import pytest
from app.ai.retrieval.ranking import DeterministicRanker
from app.ai.retrieval.models import RetrievedChunk
import uuid

def mock_chunk(score: float, heading: str = "", section: str = "", chunk_index: int = 0, vector_id: str = "") -> RetrievedChunk:
    return RetrievedChunk(
        document_id="d1",
        chunk_id=str(uuid.uuid4()),
        text="Sample text",
        similarity_score=score,
        heading=heading,
        section=section,
        chunk_index=chunk_index,
        vector_id=vector_id or str(uuid.uuid4()),
        token_count=10,
        checksum="c1"
    )

def test_rank_by_score():
    chunks = [
        mock_chunk(0.7),
        mock_chunk(0.9),
        mock_chunk(0.8)
    ]
    ranked = DeterministicRanker.rank(chunks)
    assert ranked[0].similarity_score == 0.9
    assert ranked[1].similarity_score == 0.8
    assert ranked[2].similarity_score == 0.7

def test_rank_tie_heading_match():
    chunks = [
        mock_chunk(0.8, heading="Other"),
        mock_chunk(0.8, heading="Experience")
    ]
    ranked = DeterministicRanker.rank(chunks, query_heading="Experience")
    # Both have 0.8, but index 1 matched the heading
    assert ranked[0].heading == "Experience"

def test_rank_tie_section_match():
    chunks = [
        mock_chunk(0.8, section="Misc"),
        mock_chunk(0.8, section="Skills")
    ]
    ranked = DeterministicRanker.rank(chunks, query_section="Skills")
    assert ranked[0].section == "Skills"

def test_rank_tie_chunk_index():
    chunks = [
        mock_chunk(0.8, chunk_index=5),
        mock_chunk(0.8, chunk_index=2)
    ]
    ranked = DeterministicRanker.rank(chunks)
    assert ranked[0].chunk_index == 2
    assert ranked[1].chunk_index == 5
