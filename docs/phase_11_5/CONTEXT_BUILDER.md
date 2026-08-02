# Context Builder

## Purpose
Bridges purely returned Qdrant Point Vectors into LLM-Ready text bundles. The LangGraph engine inherently relies on heavily typed schemas instead of raw string arrays. 

## Deduplication Logic
Vector Stores are prone to overlapping chunks (especially spanning multiple duplicate document uploads). 
The `ContextBuilder` traps `seen_checksums`, `seen_vector_ids`, and `seen_chunk_ids` over standard O(1) Sets, dropping identical occurrences from the response array immediately.

## Token Control
Calculates exact mathematical tokens locally via `chunk.token_count` metrics generated during Phase 11.4 uploads. Appends incrementally. If a chunk pushes total bound values over the `MAX_CONTEXT_TOKENS` configuration, the builder abruptly terminates collection cleanly without raising Exceptions, returning maximally saturated context natively.

## Context Compression (Stub)
Currently built to pass raw Validated chunks. Future versions append Redundant Sequence pruning natively into this architectural layer without rewiring search configurations.
