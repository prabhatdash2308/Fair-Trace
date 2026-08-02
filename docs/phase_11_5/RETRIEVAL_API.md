# Retrieval API

## Post Search
`POST /api/v1/retrieval/search`

Request
```json
{
  "query": "Summarize manager feedback",
  "search_mode": "STRICT",
  "document_id": "uuid-...",
  "heading": "Performance Review"
}
```
Response
```json
{
  "retrieval_id": "uuid-...",
  "query_embedding_model": "text-embedding-3-small",
  "duration_ms": 118,
  "returned_chunks": 5,
  "discarded_duplicates": 1,
  "context_tokens": 1245,
  "highest_score": 0.88,
  "lowest_score": 0.85,
  "results": [
    {
      "document_id": "uuid-...",
      "chunk_id": "uuid-...",
      "text": "Manager noted exceptional performance...",
      "similarity_score": 0.88,
      "token_count": 218,
      "checksum": "hash..."
    }
  ]
}
```

## Get Health
`GET /api/v1/retrieval/health`

Response
```json
{
  "status": "healthy",
  "duration_ms": 35,
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
    "distance": "COSINE"
  }
}
```
