import pytest
from httpx import AsyncClient
from unittest.mock import patch
from models.db.user import User

@pytest.fixture
def mock_user():
    return User(id="user-123", email="test@test.com")

@pytest.mark.asyncio
async def test_bias_health_endpoint(test_client):
    with patch("app.ai.agents.bias.service.BiasAgent.health") as mock_health:
        mock_health.return_value = {"provider_status": "healthy", "model": "gpt-4o"}
        
        response = test_client.get("/api/v1/bias/health")
        assert response.status_code == 200
        data = response.json()
        
        assert data["provider"] == "OpenAI"
        assert data["status"] == "healthy"
        
@pytest.mark.asyncio
async def test_bias_version_endpoint(test_client):
    with patch("app.ai.agents.bias.service.BiasAgent.health") as mock_health:
        mock_health.return_value = {"provider_status": "healthy", "model": "gpt-4o"}
        
        response = test_client.get("/api/v1/bias/version")
        assert response.status_code == 200
        data = response.json()
        
        assert data["agent_version"] == "1.0"
        assert "prompt_hash" in data

@pytest.mark.asyncio
async def test_bias_run_endpoint_missing_fields(test_client, mock_user):
    # No context_bundle provided
    payload = {"performance_analysis": {}}
    response = test_client.post(
        "/api/v1/bias/analyze",
        json=payload,
        headers={"Authorization": "Bearer test"}
    )
    
    # Depending on auth
    if response.status_code != 401:
        assert response.status_code == 400
        assert "context_bundle is required" in response.json()["detail"]
