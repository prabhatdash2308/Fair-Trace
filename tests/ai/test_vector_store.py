import sys
import logging

# Setup basic logging to catch output
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

from backend.app.ai.services.vector_store import (
    VectorStoreService,
    QdrantProvider,
    VectorStoreConfig,
    Telemetry,
    VectorRecord,
    VectorMetadata,
    VectorSearchRequest
)
from backend.app.ai.services.vector_store.exceptions import (
    CollectionAlreadyExistsError,
    CollectionNotFoundError
)

print("Testing Enterprise Vector Store Service...")

config = VectorStoreConfig(collection_name="test_collection")
provider = QdrantProvider()
telemetry = Telemetry()

service = VectorStoreService(
    provider=provider,
    config=config,
    telemetry=telemetry
)

print("\n1. Testing Health Check...")
if service.health_check():
    print("SUCCESS: Health check passed")
else:
    print("FAIL: Health check failed")
    sys.exit(1)

print("\n2. Testing Collection Operations...")
service.create_collection()
if service.collection_exists():
    print("SUCCESS: Collection created successfully")
else:
    print("FAIL: Collection was not created")
    sys.exit(1)

try:
    service.create_collection()
    print("FAIL: Should have raised CollectionAlreadyExistsError")
    sys.exit(1)
except CollectionAlreadyExistsError:
    print("SUCCESS: Collection duplicate check works")

print("\n3. Testing Upsert & Batch Upsert...")
r1 = VectorRecord(
    id="1", 
    vector=[1.0, 0.0, 0.0], 
    metadata=VectorMetadata(employee_id="emp-1", document_type="review")
)
r2 = VectorRecord(
    id="2", 
    vector=[0.0, 1.0, 0.0], 
    metadata=VectorMetadata(employee_id="emp-2", document_type="review")
)
r3 = VectorRecord(
    id="3", 
    vector=[0.0, 0.0, 1.0], 
    metadata=VectorMetadata(employee_id="emp-1", document_type="goal")
)

service.upsert(r1, correlation_id="req-1")
service.batch_upsert([r2, r3], correlation_id="req-2")
print("SUCCESS: Upserts executed without errors")

print("\n4. Testing Similarity Search...")
search_req = VectorSearchRequest(vector=[1.0, 0.0, 0.0], top_k=2)
res = service.search(search_req, correlation_id="req-3")
if res.matches[0].id == "1":
    print("SUCCESS: Similarity search returned expected top match")
else:
    print("FAIL: Similarity search failed")
    sys.exit(1)

print("\n5. Testing Metadata Filtering...")
# Search for vector similar to r1, but filter by emp-2 (which is r2)
search_req_filtered = VectorSearchRequest(
    vector=[1.0, 0.0, 0.0], 
    top_k=2, 
    filter={"employee_id": "emp-2"}
)
res_filtered = service.search(search_req_filtered, correlation_id="req-4")

if len(res_filtered.matches) == 1 and res_filtered.matches[0].id == "2":
    print("SUCCESS: Metadata filtering successfully restricted search space")
else:
    print("FAIL: Metadata filtering failed")
    sys.exit(1)

print("\n6. Testing Telemetry...")
if telemetry.search_count == 2 and telemetry.upsert_count == 2 and telemetry.health_checks == 1:
    print("SUCCESS: Telemetry tracked all operations")
else:
    print(f"FAIL: Telemetry mismatch. Search={telemetry.search_count}, Upsert={telemetry.upsert_count}")
    sys.exit(1)

print("\nAll verifications passed!")
