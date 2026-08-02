import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.vectorstore.qdrant_service import QdrantService
from app.vectorstore.models import VectorPoint
from app.vectorstore.exceptions import VectorValidationError, VectorCollectionError
from config import Settings
import math

@pytest.fixture
def settings():
    return Settings(
        database_url="sqlite:///./test.db",
        openai_api_key="test-key",
        jwt_secret_key="secret",
        qdrant_collection_name="test_collection"
    )

@pytest.fixture
def qdrant_service(settings):
    with patch("app.vectorstore.qdrant_service.AsyncQdrantClient"):
        yield QdrantService(settings)

def test_validate_vector_success(qdrant_service):
    # 1536 is default
    vector = [0.1] * 1536
    qdrant_service._validate_vector(vector) # Should not raise

def test_validate_vector_invalid_length(qdrant_service):
    with pytest.raises(VectorValidationError, match="dimension is 10"):
        qdrant_service._validate_vector([0.1] * 10)

def test_validate_vector_nan(qdrant_service):
    vector = [0.1] * 1535 + [math.nan]
    with pytest.raises(VectorValidationError, match="NaN or Infinity"):
        qdrant_service._validate_vector(vector)

@pytest.mark.asyncio
async def test_upsert_batch(qdrant_service):
    qdrant_service.client = AsyncMock()
    
    points = [
        VectorPoint(id="1", vector=[0.1]*1536, payload={"document_id": "1"})
    ]
    
    await qdrant_service.upsert_batch(points)
    
    qdrant_service.client.upsert.assert_called_once()
