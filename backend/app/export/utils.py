import hashlib
from typing import Dict, Any

def generate_checksum(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def generate_signature(report_json: str, workflow_id: str, approval_timestamp: str, reviewer_id: str, version: str) -> str:
    payload = f"{report_json}|{workflow_id}|{approval_timestamp}|{reviewer_id}|{version}"
    return generate_checksum(payload)
