# Phase 11.5 Changelog

## Overview
Implemented the Enterprise Semantic Retrieval Engine. Translates semantic queries securely into `ContextBundle` payloads bound securely to LangGraph integrations in Phase 11.6.

## New features
- Semantic Search (`SemanticRetriever`) implementation overriding `BaseRetriever`.
- Configurable Search Modes (`STRICT`, `BALANCED`, `EXHAUSTIVE`).
- Dynamic Qdrant query filter builder for robust Tenant/User level data isolation.
- Deterministic Ranking falling back dynamically to Heading, Section, and Position when scores align identically.
- `ContextBuilder` which validates UUIDs, extracts redundant vectors, captures checksum deduplications, and strictly asserts Token thresholds (`MAX_CONTEXT_TOKENS`).
- Added robust Retrieval metrics for debugging score variances and response latency.

## Files created
- `backend/app/ai/retrieval/base.py`
- `backend/app/ai/retrieval/context_builder.py`
- `backend/app/ai/retrieval/exceptions.py`
- `backend/app/ai/retrieval/filters.py`
- `backend/app/ai/retrieval/models.py`
- `backend/app/ai/retrieval/ranking.py`
- `backend/app/ai/retrieval/registry.py`
- `backend/app/ai/retrieval/service.py`
- `backend/routers/retrieval.py`
- `backend/tests/test_context_builder.py`
- `backend/tests/test_retrieval_filters.py`
- `backend/tests/test_retrieval_ranking.py`
- `backend/tests/test_retrieval_service.py`

## Files modified
- `backend/config.py`: Added Configuration bounds (Tokens, Strategies, Thresholds).
- `backend/main.py`: Appended Retreival HTTP router.
- `backend/models/enums.py`: Appended `SearchMode` & `RetrievalStrategy`.
- `backend/app/vectorstore/base.py`: Extended abstraction `search()`.
- `backend/app/vectorstore/qdrant_service.py`: Wrote logic wrapping `self.client.search()`.

## API changes
- **POST** `/api/v1/retrieval/search`: Search entrypoint generating `RetrievalResponse`.
- **GET** `/api/v1/retrieval/health`: Verifies Embedding Provider alongside Vector Store bindings.
