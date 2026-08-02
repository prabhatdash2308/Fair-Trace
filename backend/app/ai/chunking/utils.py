import hashlib
import tiktoken
import re
from typing import Dict, Any, Tuple, Optional
from uuid import UUID

def get_token_estimator():
    """Returns a tiktoken encoder instance."""
    # We strictly use cl100k_base as requested
    return tiktoken.get_encoding("cl100k_base")

def estimate_tokens(text: str) -> int:
    """Estimates the number of tokens in a given text using cl100k_base."""
    encoder = get_token_estimator()
    return len(encoder.encode(text, disallowed_special=()))

def generate_checksum(document_id: UUID, chunk_index: int, text: str) -> str:
    """
    Generates a stable SHA256 checksum for a chunk to prevent duplicates.
    sha256(document_id + chunk_index + text)
    """
    payload = f"{document_id}_{chunk_index}_{text}".encode('utf-8')
    return hashlib.sha256(payload).hexdigest()

def detect_document_type(text: str) -> str:
    """
    Heuristically detects the document type from the first ~1000 characters.
    """
    sample = text[:1000].lower()
    
    if any(k in sample for k in ["performance review", "annual review", "appraisal"]):
        return "Performance Review"
    elif any(k in sample for k in ["goals", "okr", "objectives"]):
        return "Goal Sheet"
    elif any(k in sample for k in ["resume", "curriculum vitae", "experience"]):
        return "Resume"
    elif any(k in sample for k in ["policy", "guidelines", "handbook"]):
        return "Policy"
    elif any(k in sample for k in ["feedback", "360 review"]):
        return "Feedback"
    
    return "Other"

def extract_hr_metadata(text: str) -> Dict[str, str]:
    """
    Uses heuristics to extract common HR metadata fields.
    """
    metadata = {}
    
    # Simple regex heuristics for name, period, manager
    name_match = re.search(r"(?i)(?:employee\s*name|name):\s*([A-Za-z\s]+)(?:\n|$)", text)
    if name_match:
        metadata["employee_name"] = name_match.group(1).strip()
        
    period_match = re.search(r"(?i)(?:review\s*period|period):\s*([0-9A-Za-z\s-]+)(?:\n|$)", text)
    if period_match:
        metadata["review_period"] = period_match.group(1).strip()
        
    manager_match = re.search(r"(?i)(?:manager|supervisor):\s*([A-Za-z\s]+)(?:\n|$)", text)
    if manager_match:
        metadata["manager_name"] = manager_match.group(1).strip()
        
    dept_match = re.search(r"(?i)(?:department|dept):\s*([A-Za-z\s&]+)(?:\n|$)", text)
    if dept_match:
        metadata["department"] = dept_match.group(1).strip()
        
    return metadata
