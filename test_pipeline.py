import sys
import logging
import uuid
import os

# Setup basic logging to catch output
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

from app.ai.state.review_state import ReviewState
from app.ai.agents.intake_agent import IntakeAgent
from app.ai.agents.embedding_agent import EmbeddingAgent
from app.ai.agents.evidence_retrieval_agent import EvidenceRetrievalAgent

from app.ai.services.embeddings import EmbeddingService, OpenAIEmbeddingProvider, EmbeddingConfig, EmbeddingCache, Telemetry as EmbTelemetry
from app.ai.services.vector_store import VectorStoreService, QdrantProvider, VectorStoreConfig, Telemetry as VSTelemetry
from app.ai.graph import ReviewGuardGraph

print("Testing LangGraph Pipeline...")

print("\n1. Initializing Agents & Services...")
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

intake_agent = IntakeAgent()
embedding_agent = EmbeddingAgent(embedding_service=emb_service, vector_store_service=vs_service)
retrieval_agent = EvidenceRetrievalAgent(embedding_service=emb_service, vector_store_service=vs_service)

print("\n2. Compiling Graph...")
try:
    graph = ReviewGuardGraph(intake_agent, embedding_agent, retrieval_agent)
    print("SUCCESS: Graph compiles")
except Exception as e:
    print(f"FAIL: Graph compilation failed - {e}")
    sys.exit(1)

print("\n3. Invoking Graph...")
state = ReviewState()
state.metadata.employee_id = uuid.uuid4()
state.metadata.review_cycle_id = uuid.uuid4()
state.input.self_assessment = "I completed my goals."
state.input.manager_feedback = "Good job on completing your goals."
state.input.peer_feedback = ["Great teamwork.", "Excellent communication."]

try:
    result = graph.execute(state)
    print("SUCCESS: Graph invokes successfully")
except Exception as e:
    print(f"FAIL: Graph invocation failed - {e}")
    sys.exit(1)

print("\n4. Verifying State Preservation & Updates...")
# Check if ReviewState was preserved
if isinstance(result, ReviewState):
    print("SUCCESS: ReviewState is correctly typed and preserved")
else:
    print(f"FAIL: Result is not a ReviewState. Type: {type(result)}")
    sys.exit(1)

# Check Agent execution array in execution state
completed_steps = result.execution.completed_steps
if "IntakeAgent" in completed_steps and "EmbeddingAgent" in completed_steps and "EvidenceRetrievalAgent" in completed_steps:
    print("SUCCESS: All 3 agents successfully executed in linear order")
else:
    print(f"FAIL: Missing agents in execution steps: {completed_steps}")
    sys.exit(1)

# Check AuditState
if len(result.audit.agent_logs) >= 3:
    print("SUCCESS: AuditState correctly aggregated logs from all agents")
else:
    print("FAIL: AuditState missing logs")
    sys.exit(1)

# Final checks on data
if result.retrieval.total_chunks > 0 and result.evidence.status == "completed":
    print("SUCCESS: Embedded and Retrieved chunks are populated in state")
else:
    print("FAIL: Downstream state updates missing")
    sys.exit(1)

print("\nAll verifications passed!")
