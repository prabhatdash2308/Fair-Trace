"""
ReviewGuard AI — LLM Client with Fallback Chain and Circuit Breaker
Implements: GPT-4o → GPT-4.1-mini → GPT-4.1-mini retry → Fail
Circuit breaker prevents cascading failures during OpenAI outages.
"""

import time
import threading
from collections import deque
from typing import Any

import structlog
from openai import OpenAI, RateLimitError, APIStatusError, APITimeoutError
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from config import settings
from core.exceptions import ModelUnavailableError, CircuitOpenError

logger = structlog.get_logger(__name__)

# ── OpenAI Client ──────────────────────────────────────────────────────────────

_openai_client: OpenAI | None = None


def get_openai_client() -> OpenAI:
    global _openai_client
    if _openai_client is None:
        _openai_client = OpenAI(api_key=settings.openai_api_key)
    return _openai_client


def get_embeddings_model() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        model=settings.openai_embedding_model,
        api_key=settings.openai_api_key,
        dimensions=settings.embedding_dimension,
    )


def get_llm(model: str | None = None, temperature: float = 0.0) -> ChatOpenAI:
    return ChatOpenAI(
        model=model or settings.openai_llm_model,
        temperature=temperature,
        api_key=settings.openai_api_key,
    )


# ── Circuit Breaker ────────────────────────────────────────────────────────────

class CircuitBreaker:
    """
    Per-model circuit breaker.
    States: CLOSED (normal) → OPEN (tripped) → HALF_OPEN (probe)
    """

    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

    def __init__(
        self,
        failure_threshold: int = 3,
        window_seconds: int = 60,
        reset_timeout: int = 30,
    ):
        self.failure_threshold = failure_threshold
        self.window_seconds = window_seconds
        self.reset_timeout = reset_timeout
        self.state = self.CLOSED
        self._failures: deque[float] = deque()
        self._opened_at: float | None = None
        self._lock = threading.Lock()

    def _prune_failures(self) -> None:
        now = time.time()
        while self._failures and now - self._failures[0] > self.window_seconds:
            self._failures.popleft()

    def is_open(self) -> bool:
        with self._lock:
            if self.state == self.CLOSED:
                return False
            if self.state == self.OPEN:
                if self._opened_at and time.time() - self._opened_at >= self.reset_timeout:
                    self.state = self.HALF_OPEN
                    return False
                return True
            return False  # HALF_OPEN allows one probe

    def record_success(self) -> None:
        with self._lock:
            self.state = self.CLOSED
            self._failures.clear()
            self._opened_at = None

    def record_failure(self) -> None:
        with self._lock:
            self._failures.append(time.time())
            self._prune_failures()
            if len(self._failures) >= self.failure_threshold:
                self.state = self.OPEN
                self._opened_at = time.time()
                logger.error("circuit_breaker_opened", failures=len(self._failures))


# Module-level circuit breakers per model
_breakers: dict[str, CircuitBreaker] = {}


def _get_breaker(model: str) -> CircuitBreaker:
    if model not in _breakers:
        _breakers[model] = CircuitBreaker(
            failure_threshold=settings.circuit_breaker_failure_threshold,
            window_seconds=settings.circuit_breaker_window_seconds,
            reset_timeout=settings.circuit_breaker_reset_timeout,
        )
    return _breakers[model]


# ── LLM Call with Fallback ─────────────────────────────────────────────────────

def call_llm_with_fallback(
    messages: list[dict[str, str]],
    response_format: dict | None = None,
    temperature: float = 0.0,
    correlation_id: str = "",
) -> tuple[str, str, dict]:
    """
    Calls LLM with fallback chain:
      GPT-4o → GPT-4.1-mini → GPT-4.1-mini (retry) → Fail

    Returns:
        (response_text, model_used, usage_dict)
        usage_dict: {prompt_tokens, completion_tokens, total_tokens, estimated_cost_usd}

    Raises:
        CircuitOpenError  — circuit breaker is open
        ModelUnavailableError — all models exhausted
    """
    models = [settings.openai_llm_model, settings.openai_fallback_model, settings.openai_fallback_model]
    client = get_openai_client()

    last_error: Exception | None = None

    for attempt, model in enumerate(models):
        breaker = _get_breaker(model)
        if breaker.is_open():
            logger.warning("circuit_breaker_skipping", model=model, attempt=attempt)
            continue

        try:
            start = time.time()
            kwargs: dict[str, Any] = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
            }
            if response_format:
                kwargs["response_format"] = response_format

            response = client.chat.completions.create(**kwargs)
            latency_ms = int((time.time() - start) * 1000)

            usage = response.usage
            cost = _estimate_cost(model, usage.prompt_tokens, usage.completion_tokens)

            breaker.record_success()
            logger.info(
                "llm_call_success",
                model=model,
                attempt=attempt,
                latency_ms=latency_ms,
                tokens=usage.total_tokens,
                correlation_id=correlation_id,
            )

            return (
                response.choices[0].message.content or "",
                model,
                {
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens,
                    "estimated_cost_usd": cost,
                    "latency_ms": latency_ms,
                    "llm_request_id": response.id,
                },
            )

        except (RateLimitError, APIStatusError, APITimeoutError) as exc:
            breaker.record_failure()
            last_error = exc
            logger.warning(
                "llm_call_failed",
                model=model,
                attempt=attempt,
                error=str(exc),
                correlation_id=correlation_id,
            )
            continue

    if any(_get_breaker(m).is_open() for m in [settings.openai_llm_model, settings.openai_fallback_model]):
        raise CircuitOpenError()
    raise ModelUnavailableError(f"All LLM models exhausted. Last error: {last_error}")


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Embeds a list of texts using the configured embedding model.
    Returns a list of embedding vectors.
    """
    client = get_openai_client()
    response = client.embeddings.create(
        model=settings.openai_embedding_model,
        input=texts,
    )
    return [item.embedding for item in response.data]


def embed_single(text: str) -> list[float]:
    """Embeds a single text string. Returns a single embedding vector."""
    return embed_texts([text])[0]


# ── Cost Estimation ────────────────────────────────────────────────────────────

# Approximate 2026 pricing per million tokens
_PRICING: dict[str, tuple[float, float]] = {
    "gpt-4o":       (5.00, 15.00),   # (input $/M, output $/M)
    "gpt-4.1-mini": (0.40, 1.60),
    "gpt-4o-mini":  (0.15, 0.60),
}


def _estimate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """Returns estimated USD cost for a single LLM call."""
    input_rate, output_rate = _PRICING.get(model, (5.00, 15.00))
    return round(
        (prompt_tokens / 1_000_000) * input_rate
        + (completion_tokens / 1_000_000) * output_rate,
        6,
    )


def llm_health_check() -> bool:
    """Returns True if a minimal LLM call succeeds. Used by /health endpoint."""
    try:
        client = get_openai_client()
        client.models.list()
        return True
    except Exception:
        return False
