# Search Architecture

## Vector Search
Searches propagate deeply through `app.vectorstore.qdrant_service.QdrantService.search()`.

## Filter Translation
`QdrantFilterBuilder` bridges pure application configurations into deeply nested `models.Filter(must=[...])` structures. 

If a query asks for `user_id` and `organization_id`, the system embeds them exactly into the Qdrant filter, assuring Qdrant executes searches strictly within boundaries rather than retrieving data, scoring it, then dropping unauthorized payloads locally (which wastes latency and costs).

## Modes
Search boundaries adjust mathematically via Enums:
- `STRICT`: Extremely high threshold (`0.85`), tight chunks (`5`). Generates incredibly exact answers for facts.
- `BALANCED`: Medium threshold (`0.75`), wider chunks (`10`). Standard synthesis configuration.
- `EXHAUSTIVE`: Loose threshold (`0.60`), max chunks (`25`). Configured for sweeping broad contextual analysis across massive documents.
