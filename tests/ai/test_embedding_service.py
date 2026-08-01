import sys
import logging

# Setup basic logging to catch output
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

from backend.app.ai.services.embeddings import (
    EmbeddingService,
    OpenAIEmbeddingProvider,
    EmbeddingConfig,
    EmbeddingCache,
    Telemetry,
    EmbeddingRequest,
    Chunker,
    ChunkingError
)

print("Testing Enterprise Embedding Service...")

config = EmbeddingConfig(chunk_size=100, chunk_overlap=20)
provider = OpenAIEmbeddingProvider()
cache = EmbeddingCache()
telemetry = Telemetry()

service = EmbeddingService(
    provider=provider,
    config=config,
    cache=cache,
    telemetry=telemetry
)

print("\n1. Testing Chunker & Metadata Preservation...")
text = "A" * 150
chunks = Chunker.chunk_text(text, 100, 20, metadata={"source": "test_doc"})
if len(chunks) == 2:
    print("SUCCESS: Chunking split text correctly (150 chars -> 2 chunks)")
else:
    print(f"FAIL: Chunking split text into {len(chunks)} chunks instead of 2")
    sys.exit(1)

if chunks[0].metadata.get("source") == "test_doc":
    print("SUCCESS: Metadata preserved in chunks")
else:
    print("FAIL: Metadata lost in chunking")
    sys.exit(1)

try:
    Chunker.chunk_text(text, 20, 20)
    print("FAIL: Should have raised ChunkingError")
    sys.exit(1)
except ChunkingError:
    print("SUCCESS: Chunking overlap validation works")

print("\n2. Testing Provider Abstraction & Service Pipeline...")
req = EmbeddingRequest(text=text, metadata={"source": "test_doc"})
res1 = service.embed(req, correlation_id="emb-1")

if len(res1.vectors) == 2:
    print("SUCCESS: Service returned correct number of embedding vectors")
else:
    print("FAIL: Service failed to return embeddings for all chunks")
    sys.exit(1)

if res1.total_tokens > 0:
    print("SUCCESS: Provider correctly recorded token usage")
else:
    print("FAIL: Token usage not recorded")

print("\n3. Testing Caching System...")
# Run again, should hit cache. Tokens should be 0 because provider isn't called.
res2 = service.embed(req, correlation_id="emb-2")
if res2.total_tokens == 0:
    print("SUCCESS: Cache hit successfully bypassed provider")
else:
    print("FAIL: Provider was called despite cache")
    sys.exit(1)

print("\n4. Testing Telemetry...")
if telemetry.total_requests == 2:
    print("SUCCESS: Telemetry recorded both requests")
else:
    print("FAIL: Telemetry missed a request")
    sys.exit(1)

print("\nAll verifications passed!")
