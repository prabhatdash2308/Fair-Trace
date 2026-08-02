import pytest
from app.ai.retrieval.filters import QdrantFilterBuilder
from app.ai.retrieval.models import RetrievalQuery
from qdrant_client.http import models as qmodels

def test_empty_query():
    query = RetrievalQuery(query="test")
    q_filter = QdrantFilterBuilder.build(query)
    assert q_filter is None

def test_full_query():
    query = RetrievalQuery(
        query="test",
        user_id="u1",
        organization_id="o1",
        document_id="d1",
        document_type="PDF",
        section="Experience",
        heading="Work History"
    )
    
    q_filter = QdrantFilterBuilder.build(query)
    assert q_filter is not None
    assert len(q_filter.must) == 6
    
    # Assert correct field binding
    fields = [c.key for c in q_filter.must]
    assert "user_id" in fields
    assert "document_type" in fields
    
def test_partial_query():
    query = RetrievalQuery(
        query="test",
        user_id="u1"
    )
    q_filter = QdrantFilterBuilder.build(query)
    assert q_filter is not None
    assert len(q_filter.must) == 1
    assert q_filter.must[0].key == "user_id"
    assert q_filter.must[0].match.value == "u1"
