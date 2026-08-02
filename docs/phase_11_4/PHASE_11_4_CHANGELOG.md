# Phase 11.4 Changelog

## Overview
Implemented the Enterprise Embedding Pipeline. Converts semantic document chunks into vector embeddings and stores them securely in Qdrant with robust validation, chunk accounting, batch processing, and provider abstraction.

## New features
- Configured Qdrant vector store connection and collection validation (`QDRANT_COLLECTION`).
- Added embedding status tracking (`QUEUED`, `PROCESSING`, `EMBEDDED`, `FAILED`).
- Created `EmbeddingProviderRegistry` to decouple from a single embedding provider.
- Created `OpenAIEmbeddingProvider` implementation using `text-embedding-3-small`.
- Implemented `Batcher` logic to safely partition chunk requests to OpenAI.
- Integrated `tenacity` retries for rate limits and upstream server errors.
- Added `/api/v1/uploads/{id}/embed` for idempotent embedding generation.
- Added `/api/v1/embeddings/health` for upstream Qdrant and OpenAI availability validation.

## Files created
- `backend/app/ai/embeddings/__init__.py`
- `backend/app/ai/embeddings/base.py`
- `backend/app/ai/embeddings/batcher.py`
- `backend/app/ai/embeddings/exceptions.py`
- `backend/app/ai/embeddings/models.py`
- `backend/app/ai/embeddings/openai_service.py`
- `backend/app/ai/embeddings/registry.py`
- `backend/app/ai/embeddings/service.py`
- `backend/app/vectorstore/__init__.py`
- `backend/app/vectorstore/base.py`
- `backend/app/vectorstore/exceptions.py`
- `backend/app/vectorstore/models.py`
- `backend/app/vectorstore/qdrant_service.py`
- `backend/routers/embeddings.py`
- `backend/tests/test_batcher.py`
- `backend/tests/test_embedding_service.py`
- `backend/tests/test_openai_provider.py`
- `backend/tests/test_qdrant.py`

## Files modified
- `backend/config.py`
- `backend/main.py`
- `backend/routers/uploads.py`
- `backend/models/enums.py`
- `backend/models/db/document_chunk.py`

## Database changes
- Upgraded `document_chunk` table with new metadata fields:
  - `embedding_status`
  - `embedding_error`
  - `embedding_provider`
  - `embedding_model`
  - `embedding_version`
  - `embedding_dimensions`
  - `embedding_checksum`
  - `embedding_duration_ms`
  - `embedding_created_at`
  - `vector_id`
  - `token_count`

## API changes
- **POST** `/api/v1/uploads/{id}/embed`: Triggers chunk vectorization.
- **GET** `/api/v1/embeddings/health`: System health assessment.

## Configuration changes
- `OPENAI_API_KEY`, `openai_embedding_model`, `openai_embedding_dimensions`, `openai_embedding_batch_size`.
- `QDRANT_URL`, `QDRANT_API_KEY`, `QDRANT_COLLECTION` (with backward compatibility).
- Added token cost mappings for OpenAI.

## Breaking changes
- None.

## Future compatibility notes
- Schema is designed strictly for multi-provider compatibility (e.g., AzureOpenAI via `BaseEmbeddingProvider` and Registry initialization).
