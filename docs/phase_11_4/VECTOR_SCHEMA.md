# Vector Schema

## Overview
The Qdrant collection relies heavily on enriched metadata payloads mapped alongside exactly `1536` floating point vectors. These payloads form the basis for upstream contextual retrieval and data-tenant isolation.

## Example payload
```json
{
  "document_id": "d98124b8-f1c2-40f4-a034-7a312015349e",
  "chunk_id": "f56b9c9d-d128-4065-9a67-d86ea5f6f690",
  "user_id": "a98827e8-e2b2-48f5-9333-8a3220455490",
  "organization_id": "org-c51152a8-f1b2-54d4-a012-7b3121113490",
  "heading": "Performance Review Q3",
  "section": "Core Competencies",
  "document_type": "PDF",
  "parser_version": "1.0",
  "chunk_version": "1.0",
  "embedding_model": "text-embedding-3-small",
  "embedding_provider": "openai",
  "checksum": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "created_at": "2026-08-02T11:04:02Z",
  "token_count": 218
}
```

## Schema Definitions
- **ID Binding**: UUIDs strictly bridge the vector points identically to Postgres table keys.
- **Tenant Isolation**: `organization_id` and `user_id` are automatically pushed by the backend API into the vector space allowing native Role-Based Access search filtering.
- **Data Integrity**: `checksum` tracks the exact hashed output of the text.
- **Provider Auditing**: Explicitly states `embedding_model` enabling safe vector migration down the line if models change.
- **Context Preservation**: Retains `heading`, `section`, and `document_type` for pre-RAG UI context rendering.
