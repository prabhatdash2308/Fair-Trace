from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
import structlog
import time

from dependencies import get_db, get_current_user
from models.db.user import User
from config import Settings, get_settings

from app.vectorstore.qdrant_service import QdrantService
from app.ai.retrieval.models import RetrievalQuery, RetrievalResponse
from app.ai.retrieval.registry import RetrieverRegistry

# Ensures implementations are registered
import app.ai.retrieval.service

router = APIRouter(prefix="/retrieval", tags=["retrieval"])
logger = structlog.get_logger(__name__)

@router.post("/search", response_model=RetrievalResponse)
async def semantic_search(
    query: RetrievalQuery,
    settings: Settings = Depends(get_settings),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Enterprise Retrieval endpoint. 
    Searches Qdrant, filters by context, scores deterministically, deduplicates, and limits context tokens.
    """
    
    # Enforce security constraints
    query.user_id = str(current_user.id)
    if hasattr(current_user, "organization_id") and current_user.organization_id:
        query.organization_id = str(current_user.organization_id)
        
    try:
        vector_store = QdrantService(settings=settings)
        # Using registry to support hybrid/keyword easily later
        retriever = RetrieverRegistry.get_retriever(
            strategy=settings.retrieval_strategy, 
            settings=settings, 
            vector_store=vector_store
        )
        
        response = await retriever.search(query)
        return response
    except Exception as e:
        logger.error("retrieval_search_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health", response_model=Dict[str, Any])
async def check_health(
    settings: Settings = Depends(get_settings),
    current_user: User = Depends(get_current_user)
):
    """
    Checks health of the Retrieval Pipeline (Embeddings + VectorStore).
    """
    start_time = time.time()
    
    # Check Vector Store
    vector_store = QdrantService(settings=settings)
    qdrant_health = await vector_store.health()
    
    # Check Embeddings via the same pipeline used for query embeds
    from app.ai.embeddings.registry import EmbeddingProviderRegistry
    import app.ai.embeddings.openai_service # register
    
    provider = EmbeddingProviderRegistry.get_provider("openai", settings=settings)
    provider_health = await provider.health()
    
    overall_status = "healthy" if provider_health.get("status") == "healthy" and qdrant_health.get("status") == "healthy" else "unhealthy"
    
    duration_ms = int((time.time() - start_time) * 1000)
    
    return {
        "status": overall_status,
        "duration_ms": duration_ms,
        "provider": provider_health,
        "vector_store": qdrant_health
    }
