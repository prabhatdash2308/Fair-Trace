"""ReviewGuard AI — Test Fixtures"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.db.base import Base
from core.database import get_db_session
from core.security import create_access_token, hash_password
from models.enums import UserRole
from main import app

# Use SQLite for tests (in-memory, no Postgres required)
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def create_test_tables():
    """Create all tables once per test session."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def test_db():
    """Provides a clean test database session, rolled back after each test."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture()
def test_client(test_db):
    """FastAPI TestClient with test DB injected."""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db_session] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def _make_token(role: UserRole, user_id: str = "00000000-0000-0000-0000-000000000001") -> str:
    return create_access_token({
        "sub": user_id,
        "email": f"{role.value.lower()}@test.com",
        "role": role.value,
        "full_name": f"Test {role.value}",
        "manager_id": None,
        "organization_id": "00000000-0000-0000-0000-000000000000",
    })


@pytest.fixture()
def admin_headers():
    return {"Authorization": f"Bearer {_make_token(UserRole.ORG_ADMIN)}"}


@pytest.fixture()
def manager_headers():
    return {"Authorization": f"Bearer {_make_token(UserRole.MANAGER, '00000000-0000-0000-0000-000000000002')}"}


@pytest.fixture()
def employee_headers():
    return {"Authorization": f"Bearer {_make_token(UserRole.EMPLOYEE, '00000000-0000-0000-0000-000000000003')}"}
