# Embedding API

## Endpoints

### `POST /api/v1/uploads/{id}/embed`

#### Request
Triggers the embedding of previously parsed and chunked documents. Idempotent action.
- **Path Variable**: `document_id` (UUID)
- **Headers**: Authorization required (Bearer Token)

#### Response
```json
{
  "status": "completed",
  "document_id": "uuid-...",
  "chunks_total": 45,
  "chunks_embedded": 45,
  "chunks_skipped": 0,
  "chunks_failed": 0,
  "batches": 1,
  "embedding_model": "text-embedding-3-small",
  "provider": "openai",
  "dimensions": 1536,
  "tokens": 4532,
  "estimated_cost_usd": 0.0000906,
  "duration_ms": 1400,
  "collection": "reviewguard_documents"
}
```

#### Errors
- `401 Unauthorized`
- `404 Not Found` (Document missing)
- `422 Unprocessable Entity` (Provider mismatch)
- `500 Internal Server Error` (Batch failure loop/Upsert rejection)

#### Authentication
Valid JWT via OAuth2 schema mapped directly to current user scopes.

#### Rate Limits
Uses underlying `tenacity` on provider calls. Client API is un-throttled natively.

#### Idempotency
Skips `EMBEDDED` and `QUEUED` records intelligently. Safely ignores already resolved embeddings unless forcefully un-resolved via DB logic.

---

### `GET /api/v1/embeddings/health`

#### Health Response
Deep assessment of downstream systems.

```json
{
  "status": "healthy",
  "duration_ms": 32,
  "provider": {
    "status": "healthy",
    "provider": "openai",
    "model": "text-embedding-3-small",
    "dimension": 1536
  },
  "vector_store": {
    "status": "healthy",
    "collection": "reviewguard_documents",
    "dimension": 1536,
    "distance": "COSINE",
    "vector_count": 8502,
    "duration_ms": 12
  }
}
```
