"""
Embedding Agent for generating vectors and upserting them to the Vector Store.
"""
import uuid
import time
from typing import List, Dict, Any, Tuple

from app.ai.base.base_agent import BaseAgent
from app.ai.base.execution_context import ExecutionContext
from app.ai.state.review_state import ReviewState
from app.ai.base.exceptions import StateValidationError

from app.ai.services.embeddings import EmbeddingService, EmbeddingRequest
from app.ai.services.vector_store import VectorStoreService, VectorRecord, VectorMetadata

class EmbeddingAgent(BaseAgent):
    """
    EmbeddingAgent orchestrates the chunking and embedding of inputs, 
    and persists them to the vector store.
    """
    def __init__(
        self, 
        embedding_service: EmbeddingService,
        vector_store_service: VectorStoreService,
        name: str = "EmbeddingAgent", 
        max_retries: int = 3
    ):
        super().__init__(name=name, max_retries=max_retries)
        self.embedding_service = embedding_service
        self.vector_store_service = vector_store_service
        
    def _validate_before_process(self, state: ReviewState) -> None:
        if not state.metadata.employee_id:
            raise StateValidationError("Missing employee_id in ReviewState.")
        if not state.metadata.review_cycle_id:
            raise StateValidationError("Missing review_cycle_id in ReviewState.")
            
    def _collect_documents(self, state: ReviewState) -> List[Tuple[str, str]]:
        """Collects all non-empty documents with their types."""
        docs = []
        if state.input.self_assessment:
            docs.append((state.input.self_assessment, "Self Assessment"))
        if state.input.manager_feedback:
            docs.append((state.input.manager_feedback, "Manager Feedback"))
            
        for peer in state.input.peer_feedback:
            docs.append((peer, "Peer Feedback"))
            
        for notes in state.input.meeting_notes:
            docs.append((notes, "Meeting Notes"))
            
        for out in state.input.project_outcomes:
            docs.append((out, "Project Outcomes"))
            
        for goal in state.input.goals:
            docs.append((goal, "Goals"))
            
        for doc in state.input.uploaded_documents:
            docs.append((doc, "Uploaded Document"))
            
        return docs

    def _process(self, state: ReviewState, context: ExecutionContext) -> ReviewState:
        # 1. Validation
        self._validate_before_process(state)
        state.retrieval.status = "processing"
        
        # 2. Collect Inputs
        docs = self._collect_documents(state)
        if not docs:
            state.audit.warnings.append(f"[{self.name}] No documents found to embed.")
            state.retrieval.status = "completed"
            return state
            
        start_time = time.perf_counter()
        
        # Ensure collection exists
        if not self.vector_store_service.collection_exists():
            self.vector_store_service.create_collection()
            
        total_chunks = 0
        vector_ids = []
        embedded_doc_types = set()
        total_cost = 0.0
        
        # 3 & 4. Embed and Upsert
        records_to_upsert: List[VectorRecord] = []
        
        for text, doc_type in docs:
            # Prepare metadata for the embedding request
            req_metadata = {
                "document_type": doc_type,
                "employee_id": str(state.metadata.employee_id),
                "review_cycle_id": str(state.metadata.review_cycle_id)
            }
            
            req = EmbeddingRequest(text=text, metadata=req_metadata)
            # Call Embedding Service
            res = self.embedding_service.embed(req, correlation_id=context.correlation_id)
            
            total_chunks += len(res.vectors)
            total_cost += res.cost
            embedded_doc_types.add(doc_type)
            
            # Map EmbeddingVectors to VectorRecords
            for emb_vec in res.vectors:
                vec_id = str(uuid.uuid4())
                vector_ids.append(vec_id)
                
                v_meta = VectorMetadata(
                    review_cycle_id=str(state.metadata.review_cycle_id),
                    employee_id=str(state.metadata.employee_id),
                    document_type=doc_type,
                    correlation_id=context.correlation_id
                )
                
                record = VectorRecord(
                    id=vec_id,
                    vector=emb_vec.vector,
                    metadata=v_meta,
                    payload={"text": emb_vec.text} # Store original text in payload
                )
                records_to_upsert.append(record)
                
        # Batch Upsert via VectorStoreService
        if records_to_upsert:
            self.vector_store_service.batch_upsert(records_to_upsert, correlation_id=context.correlation_id)
            
        # 5. State Updates
        latency_ms = int((time.perf_counter() - start_time) * 1000)
        
        # Using getattr to handle flexible property names on RetrievalState if they differ slightly
        state.retrieval.embedded_documents = list(embedded_doc_types)
        state.retrieval.total_chunks = total_chunks
        state.retrieval.vector_ids = vector_ids
        state.retrieval.collection_name = self.vector_store_service.config.collection_name
        
        # Dimension is inferred from the first vector
        if records_to_upsert:
            state.retrieval.embedding_dimension = len(records_to_upsert[0].vector)
            
        # Handle dynamic or varied naming for cost/latency in RetrievalState
        if hasattr(state.retrieval, "embedding_cost"):
            state.retrieval.embedding_cost = total_cost
        
        if hasattr(state.retrieval, "embedding_latency_ms"):
            state.retrieval.embedding_latency_ms = latency_ms
        elif hasattr(state.retrieval, "embedding_latency"):
            state.retrieval.embedding_latency = latency_ms
            
        state.retrieval.status = "completed"
        
        # Execution Metrics and Logs
        state.execution.completed_steps.append(self.name)
        state.audit.agent_logs.append(
            f"[{self.name}] Embedded {len(docs)} docs into {total_chunks} chunks. Cost: "
        )
        
        return state
