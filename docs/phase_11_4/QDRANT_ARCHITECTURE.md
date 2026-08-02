# Qdrant Architecture

## Vector Store Configuration
- **Collection**: Managed dynamically via `QDRANT_COLLECTION` (default: `reviewguard_documents`).
- **Dimension**: `1536` locked (matching `text-embedding-3-small`).
- **Cosine Distance**: Configured via Qdrant's `Distance.COSINE` configuration block.

## Payload schema
Payloads act as deep representations of origin contexts:
- `document_id` (String UUID)
- `chunk_id` (String UUID)
- `user_id` (String UUID)
- `organization_id` (String UUID, Optional)
- `heading` / `section` (Text context)
- `document_type` (Enum parsing output)
- `embedding_provider` / `embedding_model` (Source verification)
- `checksum` (Data integrity)

## Indexes
On startup, Qdrant auto-generates `KEYWORD` indexes specifically on logical grouping fields to severely reduce search latency on subsequent queries:
- `document_id`
- `chunk_id`
- `user_id`
- `organization_id`

## Metadata
Metadata tracking ensures complete transparency between database systems and isolated Qdrant containers. `token_count` and system timestamps securely align.

## Idempotent initialization
The `initialize_collection` method determines existence dynamically.
1. Does collection exist?
   - **YES**: Assert Schema (Fails execution if vector dimensionality or distance type has skewed/corrupted natively).
   - **NO**: Construct gracefully with schema settings. No forced auto-deletion. 

## Upsert flow
Vector points are instantiated, structurally validated via math models (checks against `NaN` boundaries, checks exact array lengths) then mapped into `models.PointStruct` types. The service `upserts` utilizing `wait=True` logic to verify persistence natively.
