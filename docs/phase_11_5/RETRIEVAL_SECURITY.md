# Retrieval Security

## Threat Models & Mitigations

### Cross-Tenant Retrieval
`QdrantFilterBuilder` forcibly extracts `user_id` and `organization_id` bindings straight from the JWT Authorization bindings inside the HTTP Router. Attackers cannot query documents outside of their exact bounds regardless of exact keyword match.

### Prompt Injection Persistence
The retrieval engine explicitly DOES NOT run retrieved strings back through OpenAI summarizers or interpreters. The text is passed purely back to UI rendering engines or downstream LangGraph logic safely encoded.

### Duplicate Saturation Attacks
Attackers storing millions of identical malicious phrases inside hidden files will fail to saturate the retrieval loop. `ContextBuilder` natively parses hash checks (`seen_checksums`), meaning duplicate embeddings are silently purged across the array boundary, yielding highly resilient LLM inputs.

### PII Data Leakage Logs
Raw Text strings, returned vectors, and queries are strictly stripped from all StructLog configurations. Observability exclusively monitors durations, tokens, ID strings, and mathematical thresholds securely.
