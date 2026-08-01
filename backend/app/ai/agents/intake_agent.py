"""
Intake Agent for deterministic preprocessing.
"""
import hashlib
import re
from typing import List, Optional, Set, Tuple

from app.ai.base.base_agent import BaseAgent
from app.ai.base.execution_context import ExecutionContext
from app.ai.state.review_state import ReviewState
from app.ai.base.exceptions import StateValidationError

class IntakeAgent(BaseAgent):
    """
    IntakeAgent is responsible for validating, normalizing, 
    and deduplicating all inputs before any LLM processing occurs.
    """
    def __init__(self, name: str = "IntakeAgent", max_retries: int = 0):
        # We don't need LLM or Qdrant for this agent, and no retries needed for deterministic work.
        super().__init__(name=name, max_retries=max_retries)
        self.max_payload_size = 500_000  # Example size limit
        
    def _validate_before_process(self, state: ReviewState) -> None:
        """Specific validations for Intake."""
        if not state.metadata.employee_id:
            raise StateValidationError("Missing employee_id in ReviewState.")
        if not state.metadata.review_cycle_id:
            raise StateValidationError("Missing review_cycle_id in ReviewState.")
            
    def _normalize_text(self, text: Optional[str]) -> Optional[str]:
        if not text:
            return None
        # Normalize line endings
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        # Remove trailing and leading spaces on each line
        text = "\n".join(line.strip() for line in text.split("\n"))
        # Normalize excessive whitespace
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        return text.strip()

    def _hash_text(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _process(self, state: ReviewState, context: ExecutionContext) -> ReviewState:
        # Validate inputs
        self._validate_before_process(state)
        
        seen_hashes: Set[str] = set()
        duplicates_removed = 0
        empty_removed = 0
        total_size = 0
        
        def process_field(text: Optional[str], doc_type: str) -> Optional[str]:
            nonlocal duplicates_removed, empty_removed, total_size
            if not text:
                return None
                
            normalized = self._normalize_text(text)
            if not normalized:
                empty_removed += 1
                return None
                
            text_hash = self._hash_text(normalized)
            if text_hash in seen_hashes:
                duplicates_removed += 1
                state.audit.warnings.append(f"[{self.name}] Duplicate {doc_type} detected and removed.")
                return None
                
            seen_hashes.add(text_hash)
            total_size += len(normalized)
            return normalized

        def process_list_field(texts: List[str], doc_type: str) -> List[str]:
            processed = []
            for t in texts:
                res = process_field(t, doc_type)
                if res:
                    processed.append(res)
            return processed

        # Process Single Fields
        state.input.self_assessment = process_field(state.input.self_assessment, "Self Assessment")
        state.input.manager_feedback = process_field(state.input.manager_feedback, "Manager Feedback")
        
        # Process List Fields
        state.input.peer_feedback = process_list_field(state.input.peer_feedback, "Peer Feedback")
        state.input.meeting_notes = process_list_field(state.input.meeting_notes, "Meeting Notes")
        state.input.project_outcomes = process_list_field(state.input.project_outcomes, "Project Outcomes")
        state.input.goals = process_list_field(state.input.goals, "Goals")
        
        # Process Uploaded Documents (Classification)
        classified_docs = []
        for doc in state.input.uploaded_documents:
            normalized = process_field(doc, "Uploaded Document")
            if not normalized:
                continue
                
            # Naive classification logic based on keywords
            lower_doc = normalized.lower()
            if "self assessment" in lower_doc or "my performance" in lower_doc:
                if not state.input.self_assessment:
                    state.input.self_assessment = normalized
                else:
                    state.input.self_assessment += "\n\n" + normalized
                state.audit.agent_logs.append(f"[{self.name}] Classified document as Self Assessment.")
            elif "peer review" in lower_doc or "feedback for" in lower_doc:
                state.input.peer_feedback.append(normalized)
                state.audit.agent_logs.append(f"[{self.name}] Classified document as Peer Feedback.")
            elif "goal" in lower_doc or "objective" in lower_doc:
                state.input.goals.append(normalized)
                state.audit.agent_logs.append(f"[{self.name}] Classified document as Goal.")
            else:
                classified_docs.append(normalized)
                state.audit.agent_logs.append(f"[{self.name}] Classified document as Unknown.")
                
        state.input.uploaded_documents = classified_docs
        
        if total_size > self.max_payload_size:
            raise StateValidationError(f"Total input payload size ({total_size} chars) exceeds maximum allowed ({self.max_payload_size} chars).")

        # Update ExecutionState
        state.execution.completed_steps.append(self.name)
        
        # Audit Logs
        state.audit.agent_logs.append(f"[{self.name}] Processed inputs: {duplicates_removed} duplicates removed, {empty_removed} empty inputs removed.")
        
        return state
