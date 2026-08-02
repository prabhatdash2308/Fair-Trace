"""
ReviewGuard AI — Application Configuration
Reads all settings from environment variables via Pydantic BaseSettings.
Fails fast on startup if required variables are missing.
"""

import json
from functools import lru_cache
from typing import List

from pydantic import field_validator
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

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """
        Accepts three formats from environment variables:
          1. Already a list  (when loaded from .env natively)
          2. JSON array string: '["https://foo.com","https://bar.com"]'
          3. Comma-separated:  'https://foo.com,https://bar.com'
        This is necessary because Render injects env vars as plain strings.
        """
        if isinstance(v, list):
            return v
        v = v.strip()
        if v.startswith("["):
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return [s.strip() for s in parsed]
            except json.JSONDecodeError:
                pass
        return [s.strip() for s in v.split(",") if s.strip()]

    # ── Database ───────────────────────────────────────────────────────────────
    database_url: str

    # ── Qdrant Vector Store ────────────────────────────────────────────────────
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection_name: str = "reviewguard_documents"
    
    @property
    def QDRANT_COLLECTION(self) -> str:
        return self.qdrant_collection_name
        
    vector_distance: str = "Cosine"
    upsert_batch_size: int = 100

    # ── OpenAI ────────────────────────────────────────────────────────────────
    openai_api_key: str
    openai_llm_model: str = "gpt-4o"
    openai_fallback_model: str = "gpt-4.1-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    embedding_dimension: int = 1536
    
    # ── Embedding Pipeline ────────────────────────────────────────────────────
    openai_embedding_batch_size: int = 50
    embedding_max_retries: int = 3
    embedding_timeout: int = 30

    # ── JWT ───────────────────────────────────────────────────────────────────
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 24

    # ── Pipeline ──────────────────────────────────────────────────────────────
    max_evidence_chunks: int = 5
    chunk_size_chars: int = 2000
    chunk_overlap_chars: int = 200
    similarity_threshold: float = 0.60

    # ── Document Upload & Storage ──────────────────────────────────────────────
    upload_max_size_mb: int = 25
    upload_allowed_types: List[str] = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain"
    ]
    upload_directory: str = "/tmp/reviewguard/uploads"
    temp_directory: str = "/tmp/reviewguard/temp"
    checksum_algorithm: str = "sha256"

    # ── Document Parsing ───────────────────────────────────────────────────────
    parser_timeout_seconds: int = 30
    max_pages: int = 100
    max_file_size_bytes: int = 25 * 1024 * 1024  # 25MB matches upload_max_size_mb
    max_text_size_characters: int = 500_000
    max_metadata_size_bytes: int = 50 * 1024  # 50KB

    # ── Chunking Settings ──────────────────────────────────────────────────────
    chunk_size: int = 2000
    chunk_overlap: int = 200
    min_chunk_size: int = 300
    max_chunk_size: int = 2500

    # ── Retrieval Settings ─────────────────────────────────────────────────────
    retrieval_strategy: str = "semantic"
    retrieval_top_k: int = 10
    retrieval_score_threshold: float = 0.75
    retrieval_max_context_chunks: int = 20
    max_context_tokens: int = 12000
    hybrid_search_enabled: bool = False
    rerank_enabled: bool = False

    # ── LangGraph Settings ─────────────────────────────────────────────────────
    graph_timeout_seconds: int = 300
    graph_max_retries: int = 3
    graph_checkpoint_provider: str = "memory"
    graph_enable_events: bool = True
    graph_enable_telemetry: bool = True
    graph_enable_interrupts: bool = True
    graph_enable_checkpoints: bool = True
    graph_max_node_execution_seconds: int = 60

    # ── Circuit Breaker ────────────────────────────────────────────────────────
    circuit_breaker_failure_threshold: int = 3
    circuit_breaker_window_seconds: int = 60
    circuit_breaker_reset_timeout: int = 30

    # Phase 11.7: Performance Agent
    PERFORMANCE_AGENT_MODEL: str = "gpt-4o"
    PERFORMANCE_AGENT_TIMEOUT: int = 30
    PERFORMANCE_AGENT_MAX_RETRIES: int = 1
    PERFORMANCE_AGENT_TEMPERATURE: float = 0.0
    PERFORMANCE_AGENT_MAX_TOKENS: int = 2000
    PERFORMANCE_PROMPT_VERSION: str = "1.0"
    
    # Phase 11.8: Bias Agent
    BIAS_AGENT_MODEL: str = "gpt-4o"
    BIAS_AGENT_TIMEOUT: int = 30
    BIAS_AGENT_MAX_RETRIES: int = 2
    BIAS_AGENT_MAX_TOKENS: int = 1500
    BIAS_AGENT_TEMPERATURE: float = 0.0
    BIAS_PROMPT_VERSION: str = "1.0"
    BIAS_THRESHOLD_HIGH: float = 0.75
    BIAS_THRESHOLD_MEDIUM: float = 0.50
    
    # Phase 11.9: Explainability Agent
    EXPLAINABILITY_AGENT_MODEL: str = "gpt-4o"
    EXPLAINABILITY_AGENT_TIMEOUT: int = 30
    EXPLAINABILITY_AGENT_MAX_RETRIES: int = 2
    EXPLAINABILITY_AGENT_TEMPERATURE: float = 0.0
    EXPLAINABILITY_AGENT_MAX_TOKENS: int = 2500
    EXPLAINABILITY_PROMPT_VERSION: str = "1.0"
    MAX_REASONING_STEPS: int = 25
    MAX_EVIDENCE_PER_FINDING: int = 10

    # Phase 11.10: Report Generation Agent
    REPORT_AGENT_MODEL: str = "gpt-4o"
    REPORT_AGENT_TIMEOUT: int = 45
    REPORT_AGENT_MAX_RETRIES: int = 2
    REPORT_AGENT_TEMPERATURE: float = 0.1
    REPORT_AGENT_MAX_TOKENS: int = 3500
    REPORT_PROMPT_VERSION: str = "1.0"
    MAX_REPORT_LENGTH: int = 12000
    REPORT_SCHEMA_VERSION: str = "1.0"

    # Phase 11.11: Human Approval Workflow
    GRAPH_APPROVAL_TIMEOUT: str = "72h"
    APPROVAL_REQUIRED: bool = True
    MAX_APPROVAL_RETRIES: int = 3
    ENABLE_WORKFLOW_HISTORY: bool = True
    ENABLE_AUDIT_LOG: bool = True
    ENABLE_REVIEW_NOTIFICATIONS: bool = True

    # Phase 11.12: Export Engine
    EXPORT_PROVIDER: str = "pdf"
    REPORT_TEMPLATE: str = "enterprise_v1"
    PDF_PAGE_SIZE: str = "A4"
    PDF_MARGIN_MM: int = 15
    PDF_ENABLE_DIGITAL_SIGNATURE: bool = True
    PDF_ENABLE_WATERMARK: bool = False
    PDF_FONT: str = "DejaVu Sans"
    PDF_TIMEZONE: str = "UTC"
    EXPORT_DIRECTORY: str = "exports/"

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
