# Known Limitations Phase 11.4

## Current Limitations

### Single provider (OpenAI)
Currently only `OpenAIEmbeddingProvider` is completely initialized, although the abstractions support Azure and native OSS embeddings dynamically.

### No embedding cache across documents
Identical text chunks parsed from entirely separate files will generate new distinct vector costs rather than reading cached exact matches from Qdrant.

### No async background workers
The pipeline runs linearly via the `POST` invocation thread rather than being decoupled into RabbitMQ / Celery worker instances. Large documents may block caller response.

### No streaming embeddings
Responses hold the full execution loop until completion. Clients cannot subscribe to SSE to see real-time progress of embedding batches.

### No retrieval yet
No similarity search endpoints, retrieval, or LLM integrations are exposed currently. Phase 11.4 purely writes data efficiently.

### No reranking
No Cross-Encoder or reranking algorithms are applied over the payload infrastructure natively.

### No hybrid search
BM25 lexical indexes and SPLADE sparsification are not integrated into Qdrant configurations in this phase. Currently purely Dense Vector operations.
