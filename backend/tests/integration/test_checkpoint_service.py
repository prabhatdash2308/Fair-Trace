import pytest
from app.workflows.checkpoint_service import CheckpointService

def test_checkpoint_service_initialization():
    service = CheckpointService()
    assert service.get_checkpointer() is not None

def test_checkpoint_service_stubs():
    assert CheckpointService.list("thread_id") == []
    assert CheckpointService.exists("thread_id", "cp_id") is False
    assert CheckpointService.cleanup_expired(30) == 0
