import pytest
from app.ai.graph.state import ReviewState

def test_state_initialization():
    state: ReviewState = {
        "execution_id": "test-123",
        "document_id": "doc-1",
        "user_id": "usr-1",
        "organization_id": "org-1",
        "context_bundle": {"text": "hello"}
    }
    
    assert state["execution_id"] == "test-123"
    assert "metadata" not in state
    
def test_state_mutation():
    state: ReviewState = {
        "execution_id": "test-123",
        "document_id": "doc-1",
        "user_id": "usr-1",
        "context_bundle": {}
    }
    
    # Simulate middleware injecting metadata
    state["metadata"] = {"current_node": "load_context"}
    
    assert state["metadata"]["current_node"] == "load_context"
