"""
Bootstrap factory for AI services.
"""
import os
from pathlib import Path

from app.ai.services.llm.llm_service import LLMService
from app.ai.services.llm.config import LLMConfig
from app.ai.services.llm.circuit_breaker import CircuitBreaker
from app.ai.services.llm.retry import RetryManager
from app.ai.services.llm.telemetry import Telemetry as LLMTelemetry

from app.ai.services.embeddings.embedding_service import EmbeddingService
from app.ai.services.embeddings.config import EmbeddingConfig
from app.ai.services.embeddings.cache import EmbeddingCache
from app.ai.services.embeddings.telemetry import Telemetry as EmbeddingTelemetry

from app.ai.services.vector_store.vector_store_service import VectorStoreService
from app.ai.services.vector_store.config import VectorStoreConfig
from app.ai.services.vector_store.telemetry import Telemetry as VectorStoreTelemetry

from app.ai.prompts.registry import PromptRegistry
from app.ai.prompts.loader import PromptLoader

from app.ai.bootstrap.provider_factory import (
    llm_provider,
    embedding_provider,
    vector_store_provider
)

llm_service = LLMService(
    provider=llm_provider,
    config=LLMConfig(),
    circuit_breaker=CircuitBreaker(),
    retry_manager=RetryManager(),
    telemetry=LLMTelemetry()
)

embedding_service = EmbeddingService(
    provider=embedding_provider,
    config=EmbeddingConfig(),
    cache=EmbeddingCache(),
    telemetry=EmbeddingTelemetry()
)

vector_store_service = VectorStoreService(
    provider=vector_store_provider,
    config=VectorStoreConfig(collection_name="reviewguard_documents"),
    telemetry=VectorStoreTelemetry()
)

base_dir = Path(os.path.abspath(__file__)).parent.parent / "prompts"
prompt_registry = PromptRegistry(loader=PromptLoader(base_dir=base_dir))
