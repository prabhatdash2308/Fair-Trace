# Retrieval Architecture

## Goal
Abstract complex semantic vector retrieval away from standard Router loops while generating LLM-ready Contexts independently of RAG execution paths.

## Abstractions

### RetrieverRegistry
Enables dynamically replacing the core Retrieval mechanism:
- `semantic`: Configured currently. Converts strings directly into OpenAi vectors then sweeps Qdrant using COSINE distance logic.
- `hybrid` (Future): Could instantiate multiple passes (BM25 + Dense) and merge results mathematically via Reciprocal Rank Fusion.
- `keyword` (Future): Subverts dense vectors entirely via payload exact match parsing.

### BaseRetriever
Defines `search()` mapping down to primitive `RetrievalResponse` JSON APIs for UI preview modes, and `build_context()` mapping purely to `ContextBundle` models targeting backend AI loops natively.

### Embedding Integration
Reuses the `EmbeddingProviderRegistry` and `OpenAIEmbeddingProvider` classes constructed in Phase 11.4 to embed queries, assuring mathematically identical tokenizing bounds, model names, and dimensions without duplicating logic paths.
