import sys
import logging
import uuid

# Setup basic logging to catch output
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

from app.ai.state.review_state import ReviewState
from app.ai.base.exceptions import StateValidationError
from app.ai.base.base_agent import BaseAgent
from app.ai.base.execution_context import ExecutionContext

from app.ai.services.embeddings import EmbeddingService, OpenAIEmbeddingProvider, EmbeddingConfig, EmbeddingCache, Telemetry as EmbTelemetry
from app.ai.services.vector_store import VectorStoreService, QdrantProvider, VectorStoreConfig, Telemetry as VSTelemetry
from app.ai.agents.embedding_agent import EmbeddingAgent

print("Testing Embedding Agent...")

print("\n1. Testing Inheritance...")
if issubclass(EmbeddingAgent, BaseAgent):
    print("SUCCESS: EmbeddingAgent inherits from BaseAgent")
else:
    print("FAIL: EmbeddingAgent does not inherit from BaseAgent")
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

agent = EmbeddingAgent(
    embedding_service=emb_service,
    vector_store_service=vs_service
)

print("\n2. Testing Validation...")
state = ReviewState()
# Ensure state fails if empty ids
try:
    agent.execute(state)
    print("FAIL: Should have raised validation error for missing IDs")
    sys.exit(1)
except StateValidationError:
    print("SUCCESS: Validation intercepted missing IDs")
    
state.metadata.employee_id = uuid.uuid4()
state.metadata.review_cycle_id = uuid.uuid4()

print("\n3. Testing Service Orchestration & State Updates...")
# Add some documents
state.input.self_assessment = "Self assessment doc content." * 5  # enough to generate some chunks
state.input.peer_feedback = ["Peer feedback 1", "Peer feedback 2"]

result = agent.execute(state)

# Check Retrieval State
if result.retrieval.status == "completed":
    print("SUCCESS: Retrieval state status updated")
else:
    print("FAIL: Retrieval state status incorrect")
    sys.exit(1)

if result.retrieval.total_chunks > 0:
    print(f"SUCCESS: Total chunks recorded: {result.retrieval.total_chunks}")
else:
    print("FAIL: Chunks not recorded")
    sys.exit(1)

if len(result.retrieval.vector_ids) == result.retrieval.total_chunks:
    print("SUCCESS: Vector IDs accurately tracked")
else:
    print("FAIL: Vector IDs mismatch")
    sys.exit(1)

if result.retrieval.collection_name == "test_collection":
    print("SUCCESS: Collection name recorded")
else:
    print("FAIL: Collection name missing")

# Check Audit & Execution
if "EmbeddingAgent" in result.execution.completed_steps:
    print("SUCCESS: Execution metrics recorded")
else:
    print("FAIL: Execution state not updated")
    sys.exit(1)

if len(result.audit.agent_logs) > 0:
    print("SUCCESS: AuditState updated with logs")
else:
    print("FAIL: AuditState not updated")
    sys.exit(1)

print("\n4. Testing VectorStore Persistence...")
if vs_service.collection_exists():
    print("SUCCESS: Vector Store collection created automatically")
else:
    print("FAIL: Vector Store collection not created")
    sys.exit(1)

print("\nAll verifications passed!")
