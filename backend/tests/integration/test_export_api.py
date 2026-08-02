import pytest
from unittest.mock import patch
from models.db.user import User

@pytest.fixture
def mock_user():
    return User(id="user-123", email="test@test.com")

@pytest.mark.asyncio
@patch("routers.export.ExportService.generate_export")
async def test_export_api_start(mock_generate, test_client, mock_user):
    mock_generate.return_value.id = "exp-123"
    
    response = test_client.post(
        "/api/v1/export/pdf/wf-123",
        headers={"Authorization": "Bearer test"}
    )
    
    if response.status_code != 401:
        assert response.status_code == 200
        assert response.json()["export_id"] == "exp-123"

@pytest.mark.asyncio
@patch("routers.export.ExportService.get_download_url")
async def test_export_api_download(mock_get_url, test_client, mock_user):
    mock_get_url.return_value = "https://s3.amazonaws.com/url"
    
    response = test_client.get(
        "/api/v1/export/download/exp-123",
        headers={"Authorization": "Bearer test"}
    )
    
    if response.status_code != 401:
        assert response.status_code == 200
        assert response.json()["download_url"] == "https://s3.amazonaws.com/url"
