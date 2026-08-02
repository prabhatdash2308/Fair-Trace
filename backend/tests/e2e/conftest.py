import os
import pytest
from typing import Dict, Any
from unittest.mock import patch
from tests.e2e.utils.mock_openai import MockOpenAI
from tests.e2e.utils.mock_qdrant import MockQdrantClient

# Ensure correct execution mode
MODE = os.getenv("MODE", "mock")

@pytest.fixture(scope="session", autouse=True)
def apply_mocks_if_needed():
    if MODE == "mock":
        with patch("openai.AsyncOpenAI", new=MockOpenAI), \
             patch("app.vectorstore.qdrant_service.AsyncQdrantClient", new=MockQdrantClient):
            yield
    else:
        yield

@pytest.fixture(scope="session")
def e2e_mode() -> str:
    return MODE

@pytest.fixture
def api_client():
    from fastapi.testclient import TestClient
    from main import app
    
    with TestClient(app) as client:
        yield client

@pytest.fixture
def auth_headers() -> Dict[str, str]:
    if MODE == "mock":
        return {"Authorization": "Bearer test_admin_token"}
    else:
        return {"Authorization": "Bearer test_admin_token"}
