from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
import structlog
import time

from dependencies import get_db, get_current_user
from models.db.user import User
from config import Settings, get_settings
from app.vectorstore.qdrant_service import QdrantService
from app.ai.embeddings.registry import EmbeddingProviderRegistry
from app.ai.embeddings.openai_service import OpenAIEmbeddingProvider

router = APIRouter(prefix="/embeddings", tags=["embeddings"])
logger = structlog.get_logger(__name__)

@router.get("/health", response_model=Dict[str, Any])
async def check_health(
    settings: Settings = Depends(get_settings),
    current_user: User = Depends(get_current_user)
):
    """
    Checks health of the entire Embedding Pipeline.
    Validates OpenAI API reachability and Qdrant readiness.
    """
    start_time = time.time()
    
    # Check Provider
    provider = EmbeddingProviderRegistry.get_provider("openai", settings=settings)
    provider_health = await provider.health()
    
    # Check Vector Store
    vector_store = QdrantService(settings=settings)
    qdrant_health = await vector_store.health()
    
    overall_status = "healthy" if provider_health.get("status") == "healthy" and qdrant_health.get("status") == "healthy" else "unhealthy"
    
    duration_ms = int((time.time() - start_time) * 1000)
    
    return {
        "status": overall_status,
        "duration_ms": duration_ms,
        "provider": provider_health,
        "vector_store": qdrant_health
    }
