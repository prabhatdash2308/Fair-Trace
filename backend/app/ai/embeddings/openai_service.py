import time
from typing import List, Dict, Any
import structlog
from openai import AsyncOpenAI
import openai
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.ai.embeddings.base import BaseEmbeddingProvider
from app.ai.embeddings.models import ChunkToEmbed, BatchEmbeddingResponse, EmbeddingVector, TokenAccounting
from app.ai.embeddings.exceptions import (
    ProviderAuthenticationError,
    RateLimitExceededError,
    ProviderTimeoutError,
    EmbeddingError
)
from app.ai.embeddings.registry import EmbeddingProviderRegistry
from config import Settings

logger = structlog.get_logger(__name__)

class OpenAIEmbeddingProvider(BaseEmbeddingProvider):
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            timeout=float(settings.embedding_timeout)
        )
        self._provider_name = "OpenAI"
        self._model_name = settings.openai_embedding_model
        self._dimension = settings.embedding_dimension
        self._version = "1.0"

    @property
    def provider_name(self) -> str:
        return self._provider_name

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def model_version(self) -> str:
        return self._version

    @property
    def dimension(self) -> int:
        return self._dimension

    def _should_retry(exception: BaseException) -> bool:
        if isinstance(exception, (openai.RateLimitError, openai.APIConnectionError, openai.InternalServerError)):
            return True
        return False

    @retry(
        retry=retry_if_exception_type((openai.RateLimitError, openai.APIConnectionError, openai.InternalServerError)),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        stop=stop_after_attempt(3),
        reraise=True
    )
    async def _call_openai(self, texts: List[str]) -> Any:
        return await self.client.embeddings.create(
            input=texts,
            model=self.model_name,
            dimensions=self.dimension
        )

    async def embed_batch(self, chunks: List[ChunkToEmbed]) -> BatchEmbeddingResponse:
        start_time = time.time()
        
        # Order-preserving extraction
        texts = [chunk.text for chunk in chunks]
        
        try:
            response = await self._call_openai(texts)
            
            vectors = []
            for i, data in enumerate(response.data):
                # The response.data array aligns with input array
                vectors.append(EmbeddingVector(
                    chunk_id=chunks[i].chunk_id,
                    vector=data.embedding,
                    token_count=0  # OpenAI doesn't return per-chunk tokens in embedding response
                ))
            
            total_tokens = response.usage.total_tokens
            prompt_tokens = response.usage.prompt_tokens
            
            # Approximate cost for text-embedding-3-small (e.g., $0.02 / 1M tokens)
            cost = (prompt_tokens / 1_000_000) * 0.02
            
            accounting = TokenAccounting(
                total_tokens=total_tokens,
                prompt_tokens=prompt_tokens,
                estimated_cost_usd=cost
            )
            
            duration_ms = int((time.time() - start_time) * 1000)
            
            return BatchEmbeddingResponse(
                vectors=vectors,
                accounting=accounting,
                model=self.model_name,
                provider=self.provider_name,
                version=self.model_version,
                duration_ms=duration_ms
            )

        except openai.AuthenticationError as e:
            logger.error("openai_auth_error", error=str(e))
            raise ProviderAuthenticationError("OpenAI authentication failed") from e
        except openai.RateLimitError as e:
            logger.error("openai_rate_limit_error", error=str(e))
            raise RateLimitExceededError("OpenAI rate limit exceeded after retries") from e
        except openai.APITimeoutError as e:
            logger.error("openai_timeout_error", error=str(e))
            raise ProviderTimeoutError("OpenAI request timed out") from e
        except Exception as e:
            logger.error("openai_unknown_error", error=str(e))
            raise EmbeddingError(f"OpenAI embedding failed: {str(e)}") from e

    async def health(self) -> Dict[str, Any]:
        start_time = time.time()
        try:
            # Minimal health check
            await self.client.models.retrieve(self.model_name)
            duration_ms = int((time.time() - start_time) * 1000)
            return {
                "status": "healthy",
                "provider": self.provider_name,
                "model": self.model_name,
                "duration_ms": duration_ms
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "provider": self.provider_name,
                "error": str(e)
            }

EmbeddingProviderRegistry.register("openai", OpenAIEmbeddingProvider)
