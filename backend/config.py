"""
ReviewGuard AI — Application Configuration
Reads all settings from environment variables via Pydantic BaseSettings.
Fails fast on startup if required variables are missing.
"""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ── Application ────────────────────────────────────────────────────────────
    app_name: str = "ReviewGuard AI"
    app_version: str = "1.0.0"
    environment: str = "development"
    cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # ── Database ───────────────────────────────────────────────────────────────
    database_url: str

    # ── Qdrant Vector Store ────────────────────────────────────────────────────
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection_name: str = "reviewguard_documents"

    # ── OpenAI ────────────────────────────────────────────────────────────────
    openai_api_key: str
    openai_llm_model: str = "gpt-4o"
    openai_fallback_model: str = "gpt-4.1-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    embedding_dimension: int = 1536

    # ── JWT ───────────────────────────────────────────────────────────────────
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 24

    # ── Pipeline ──────────────────────────────────────────────────────────────
    max_evidence_chunks: int = 5
    chunk_size_chars: int = 2000
    chunk_overlap_chars: int = 200
    similarity_threshold: float = 0.60

    # ── Circuit Breaker ────────────────────────────────────────────────────────
    circuit_breaker_failure_threshold: int = 3
    circuit_breaker_window_seconds: int = 60
    circuit_breaker_reset_timeout: int = 30

    @property
    def is_development(self) -> bool:
        return self.environment == "development"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance — reads .env once at startup."""
    return Settings()


# Module-level settings instance for direct import
settings = get_settings()
