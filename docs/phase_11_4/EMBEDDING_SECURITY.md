# Embedding Security

## Policies & Protections

### API key protection
- `OPENAI_API_KEY` is loaded dynamically from environmental overlays.
- Pydantic Settings strictly block key leakage into application log outputs.

### Retry policy
- Defends against upstream OpenAI throttling by utilizing `tenacity` exponential backoffs, explicitly trapping `429 Too Many Requests` or `5xx Server Errors` over standard runtime timeouts.

### Timeout policy
- Network operations against upstream vector stores (Qdrant) and LLM providers execute strictly over `asyncio` timeouts minimizing server thread starvation during upstream degradation.

### No chunk logging
- Raw document strings (which may contain PII, SSNs, PHI, or sensitive financial statements) are strictly purged from system stdout and log ingestors during embedding execution.

### Checksum idempotency
- Extracted cryptographic checksums map to the underlying chunk payload. Re-embedding loops ignore identical text hashes resolving infinite recursion abuse vectors.

### Vector validation
- Mathematical safety boundaries trap broken vectors (`NaN` or `Infinity` indices) pre-upsert, circumventing Qdrant index poisoning.

### Payload validation
- Schema sizes confirm the exact 1536 standard size requested prior to network serialization, isolating structural defects.

### Duplicate prevention
- UUIDs for embeddings bind strictly 1:1 against their database parent ID chunks. Re-upserts simply merge over the index rather than multiplying duplicate vectors across Qdrant space.
