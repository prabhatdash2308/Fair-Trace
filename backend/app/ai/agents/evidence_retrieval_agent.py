"""
Evidence Retrieval Agent for deterministic vector search and retrieval.
"""
import time
from typing import List, Dict, Any

from app.ai.base.base_agent import BaseAgent
from app.ai.base.execution_context import ExecutionContext
from app.ai.state.review_state import ReviewState
from app.ai.base.exceptions import StateValidationError

from app.ai.services.embeddings import EmbeddingService, EmbeddingRequest
from app.ai.services.vector_store import VectorStoreService, VectorSearchRequest, SearchMatch

class EvidenceRetrievalAgent(BaseAgent):
    """
    EvidenceRetrievalAgent executes semantic searches against the Vector Store
    to retrieve grounded evidence for downstream agents.
    """
    def __init__(
        self, 
        embedding_service: EmbeddingService,
        vector_store_service: VectorStoreService,
        name: str = "EvidenceRetrievalAgent", 
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
            
    def _generate_queries(self, state: ReviewState) -> List[str]:
        """
        Generate static/semantic queries for deterministic retrieval.
        No LLM is used.
        """
        return [
            "Performance achievements, goals, and positive feedback",
            "Areas for improvement, growth, and critical feedback",
            "Peer and manager evaluations regarding behavior and outcomes"
        ]

    def _process(self, state: ReviewState, context: ExecutionContext) -> ReviewState:
        # 1. Validation
        self._validate_before_process(state)
        state.evidence.status = "processing"
        
        start_time = time.perf_counter()
        
        # Ensure collection exists
        if not self.vector_store_service.collection_exists():
            state.audit.warnings.append(f"[{self.name}] Collection does not exist. Skipping retrieval.")
            state.evidence.status = "completed"
            return state
            
        queries = self._generate_queries(state)
        all_matches: List[SearchMatch] = []
        total_cost = 0.0
        
        # Set up filters
        metadata_filter = {
            "employee_id": str(state.metadata.employee_id),
            "review_cycle_id": str(state.metadata.review_cycle_id)
        }
        
        # 2 & 3. Orchestrate Search
        for query in queries:
            # Generate query embedding
            req = EmbeddingRequest(text=query)
            res = self.embedding_service.embed(req, correlation_id=context.correlation_id)
            total_cost += res.cost
            
            # Assume 1 vector returned for a single query string
            query_vector = res.vectors[0].vector
            
            search_req = VectorSearchRequest(
                vector=query_vector,
                top_k=5,
                filter=metadata_filter,
                score_threshold=0.60
            )
            
            # Execute search
            search_res = self.vector_store_service.search(search_req, correlation_id=context.correlation_id)
            all_matches.extend(search_res.matches)
            
        # 4. Deduplicate and Sort
        unique_matches: Dict[str, SearchMatch] = {}
        for match in all_matches:
            # Deduplicate by vector/record ID, keeping highest score
            if match.id not in unique_matches or match.score > unique_matches[match.id].score:
                unique_matches[match.id] = match
                
        # Sort descending by similarity
        sorted_matches = sorted(unique_matches.values(), key=lambda x: x.score, reverse=True)
        
        # 5. Populate State
        latency_ms = int((time.perf_counter() - start_time) * 1000)
        
        retrieved_chunks = []
        citations = []
        scores = []
        top_matches_dicts = []
        doc_sources = set()
        
        for m in sorted_matches:
            chunk_text = m.payload.get("text", "")
            doc_type = m.metadata.document_type
            
            retrieved_chunks.append(chunk_text)
            doc_sources.add(doc_type)
            scores.append(m.score)
            
            citations.append(f"[{doc_type}] {chunk_text[:50]}...")
            
            top_matches_dicts.append({
                "employee_id": m.metadata.employee_id,
                "review_cycle_id": m.metadata.review_cycle_id,
                "document_type": m.metadata.document_type,
                "chunk_id": m.metadata.chunk_id,
                "vector_id": m.id,
                "similarity_score": m.score,
                "source_document": m.metadata.source,
                "timestamp": str(m.metadata.created_at) if m.metadata.created_at else None,
                "content": chunk_text
            })
            
        state.evidence.retrieved_chunks = retrieved_chunks
        state.evidence.retrieved_documents = list(doc_sources)
        state.evidence.citations = citations
        state.evidence.similarity_scores = scores
        state.evidence.evidence_count = len(sorted_matches)
        state.evidence.top_matches = top_matches_dicts
        state.evidence.retrieval_cost = total_cost
        state.evidence.retrieval_latency_ms = latency_ms
        state.evidence.status = "completed"
        
        # 6. Execution and Audit Logs
        state.execution.completed_steps.append(self.name)
        state.audit.agent_logs.append(
            f"[{self.name}] Retrieved {len(sorted_matches)} chunks. Cost: "
        )
        
        return state
