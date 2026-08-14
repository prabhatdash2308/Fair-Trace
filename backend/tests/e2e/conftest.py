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

from core.database import get_db_session
from models.db.user import User
from models.db.organization import Organization
from core.security import hash_password

@pytest.fixture
def api_client(test_db):
    from fastapi.testclient import TestClient
    from main import app
    
    import uuid
    
    # Seed the test DB with the organization and user
    org_id = uuid.UUID("00000000-0000-0000-0000-000000000000")
    user_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
    
    org = Organization(id=org_id, name="Test Org")
    test_db.add(org)
    
    user = User(
        id=user_id,
        email="admin@test.com",
        password_hash=hash_password("password"),
        full_name="Test Admin",
        role=UserRole.ORG_ADMIN,
        organization_id=org_id
    )
    test_db.add(user)
    test_db.commit()

    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db_session] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

from core.security import create_access_token
from models.enums import UserRole

def _make_token(role: UserRole, user_id: str = "00000000-0000-0000-0000-000000000001") -> str:
    return create_access_token({
        "sub": user_id,
        "email": f"{role.value.lower()}@test.com",
        "role": role.value,
        "full_name": f"Test {role.value}",
        "manager_id": None,
        "organization_id": "00000000-0000-0000-0000-000000000000",
    })

@pytest.fixture
def auth_headers() -> Dict[str, str]:
    return {"Authorization": f"Bearer {_make_token(UserRole.ORG_ADMIN)}"}
