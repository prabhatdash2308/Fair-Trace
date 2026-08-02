# Known Limitations Phase 11.5

## Current Limitations

### Exact Duplicates Handling
Currently `ContextBuilder` purges duplicates blindly based purely on exact checksum identity mappings. Sub-word edits in different document uploads will map to distinct `seen_checksums` and thus inject practically identical meanings natively across LLM windows. Real Compression algorithms in later phases must resolve semantic redundancy natively.

### Hybrid Search Dummy
While the Registry design maps explicitly to `hybrid` overrides, currently `SemanticRetriever` executes densely 100%. BM25 indexes are entirely unsupported by the Qdrant connection configuration locally.

### Context Limits
The system truncates contexts extremely violently by just breaking the `for` loops rather than performing summarization or progressive chunk scaling. Long queries requesting exhaustive analysis will hit invisible memory ceilings.

### Reciprocal Rank Fusion
Results returned via search are natively trusted by their dense scores. Reranking using Cross-Encoders (e.g. `bge-reranker-large`) or combining sparse matches via RRF scores is unsupported.
