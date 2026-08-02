# Cost Accounting

## Token Accounting
Tokens are counted accurately by trapping the underlying provider's (`OpenAI`) `response.usage.total_tokens` blocks rather than relying on local `tiktoken` approximations, guaranteeing 100% accurate system tracking.

## Estimated Costs
Costs are evaluated natively inside the provider abstraction per batch calculation mapping the upstream tokens to static billing logic.

### Provider
`openai`

### Model
`text-embedding-3-small` (Baseline configuration).

### Duration
Duration tracking runs specifically wrapped over the `start_time` and `end_time` logic within the orchestration block generating highly accurate system timings across network spans. 

### Retries
Tenacity backoff intervals (`Retry`) handle 429 timeouts natively without dropping upstream cost variables or failing entire payloads, generating highly resilient token captures.

## Future Billing Strategy
The `DocumentChunk` table holds aggregate cost sums per chunk. In subsequent analytics updates, these fields can be queried collectively using SQL aggregation:
```sql
SELECT SUM(token_count) as total_tokens, 
       SUM(estimated_cost_usd) as document_cost 
FROM document_chunks 
WHERE document_id = 'xxx';
```
This enables organization-level invoice billing per uploaded document effortlessly.
