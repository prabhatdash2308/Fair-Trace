import sys
import logging
import uuid

# Setup basic logging to catch output
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

from app.ai.state.review_state import ReviewState
from app.ai.base.exceptions import StateValidationError
from app.ai.base.base_agent import BaseAgent

from app.ai.services.embeddings import EmbeddingService, OpenAIEmbeddingProvider, EmbeddingConfig, EmbeddingCache, Telemetry as EmbTelemetry
from app.ai.services.vector_store import VectorStoreService, QdrantProvider, VectorStoreConfig, Telemetry as VSTelemetry, VectorRecord, VectorMetadata
from app.ai.agents.evidence_retrieval_agent import EvidenceRetrievalAgent

print("Testing Evidence Retrieval Agent...")

print("\n1. Testing Inheritance...")
if issubclass(EvidenceRetrievalAgent, BaseAgent):
    print("SUCCESS: EvidenceRetrievalAgent inherits from BaseAgent")
else:
    print("FAIL: EvidenceRetrievalAgent does not inherit from BaseAgent")
    sys.exit(1)

# Setup mock services
emb_service = EmbeddingService(
    provider=OpenAIEmbeddingProvider(),
    config=EmbeddingConfig(chunk_size=100, chunk_overlap=20),
    cache=EmbeddingCache(),
    telemetry=EmbTelemetry()
)

vs_service = VectorStoreService(
    provider=QdrantProvider(),
    config=VectorStoreConfig(collection_name="test_collection"),
    telemetry=VSTelemetry()
)
vs_service.create_collection()

agent = EvidenceRetrievalAgent(
    embedding_service=emb_service,
    vector_store_service=vs_service
)

state = ReviewState()
state.metadata.employee_id = uuid.uuid4()
state.metadata.review_cycle_id = uuid.uuid4()

print("\n2. Seeding Vector Database for Test...")
# Seed a few vectors with the same employee_id to test retrieval
vec_id_1 = str(uuid.uuid4())
r1 = VectorRecord(
    id=vec_id_1,
    vector=[0.1, 0.2, 0.3], # Remember OpenAIEmbeddingProvider mock outputs [0.1, 0.2, 0.3], so score will be very high (0.14) Wait. dot product = 0.01+0.04+0.09 = 0.14. 
    # Ah, if threshold is 0.60, it will filter it out! Let me seed with higher values. 1.0, 1.0, 1.0 -> dot product = 0.1+0.2+0.3 = 0.6
    metadata=VectorMetadata(employee_id=str(state.metadata.employee_id), review_cycle_id=str(state.metadata.review_cycle_id), document_type="Peer Feedback"),
    payload={"text": "Excellent teamwork and communication."}
)
r2 = VectorRecord(
    id=str(uuid.uuid4()),
    vector=[10.0, 10.0, 10.0], # Very high score to pass 0.60 threshold
    metadata=VectorMetadata(employee_id=str(state.metadata.employee_id), review_cycle_id=str(state.metadata.review_cycle_id), document_type="Self Assessment"),
    payload={"text": "I met all my goals."}
)
# Wrong employee id (should be filtered out)
r3 = VectorRecord(
    id=str(uuid.uuid4()),
    vector=[10.0, 10.0, 10.0],
    metadata=VectorMetadata(employee_id=str(uuid.uuid4()), review_cycle_id=str(state.metadata.review_cycle_id), document_type="Goals"),
    payload={"text": "This should not be retrieved."}
)

vs_service.batch_upsert([r1, r2, r3], correlation_id="seed")

print("\n3. Testing Retrieval & State Updates...")
result = agent.execute(state)

# Check Evidence State
if result.evidence.status == "completed":
    print("SUCCESS: Evidence state status updated")
else:
    print("FAIL: Evidence state status incorrect")
    sys.exit(1)

if result.evidence.evidence_count > 0:
    print(f"SUCCESS: Evidence count recorded: {result.evidence.evidence_count}")
else:
    print("FAIL: No evidence recorded (Check threshold or metadata filter)")
    sys.exit(1)

# Check deduplication and metadata filtering
retrieved_texts = [m["content"] for m in result.evidence.top_matches]
if "This should not be retrieved." in retrieved_texts:
    print("FAIL: Metadata filter failed. Retrieved wrong employee.")
    sys.exit(1)
else:
    print("SUCCESS: Metadata filtering successfully excluded wrong employee")

# Check Deduplication (should only have 1 or 2 chunks depending on score)
if len(result.evidence.top_matches) <= 2:
    print("SUCCESS: Deduplication across multiple queries works")
else:
    print("FAIL: Deduplication failed")
    sys.exit(1)

if len(result.evidence.retrieved_chunks) > 0 and len(result.evidence.similarity_scores) > 0:
    print("SUCCESS: Chunks, citations, and scores correctly populated")
else:
    print("FAIL: Missing chunks or scores in state")
    sys.exit(1)

# Check Audit & Execution
if "EvidenceRetrievalAgent" in result.execution.completed_steps:
    print("SUCCESS: Execution metrics recorded")
else:
    print("FAIL: Execution state not updated")
    sys.exit(1)

if len(result.audit.agent_logs) > 0:
    print("SUCCESS: AuditState updated with logs")
else:
    print("FAIL: AuditState not updated")
    sys.exit(1)

print("\nAll verifications passed!")
