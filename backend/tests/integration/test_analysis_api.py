import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from models.db.user import User

@pytest.fixture
def mock_user():
    return User(id="user-123", email="test@test.com")

@pytest.mark.asyncio
async def test_performance_health_endpoint(test_client):
    with patch("app.ai.agents.performance.service.PerformanceAgent.health") as mock_health:
        mock_health.return_value = {"provider_status": "healthy", "model": "gpt-4o"}
        
        response = test_client.get("/api/v1/analysis/performance/health")
        assert response.status_code == 200
        data = response.json()
        
        assert data["provider"] == "OpenAI"
        assert data["model"] == "gpt-4o"
        assert data["provider_status"] == "healthy"

@pytest.mark.asyncio
async def test_performance_run_endpoint_missing_bundle(test_client, mock_user):
    # No context_bundle provided
    payload = {}
    response = test_client.post(
        "/api/v1/analysis/performance",
        json=payload,
        headers={"Authorization": "Bearer test"}
    )
    
    # 400 or 401 depending on auth overrides, assuming auth passes:
    if response.status_code != 401:
        assert response.status_code == 400
        assert "context_bundle is required" in response.json()["detail"]
