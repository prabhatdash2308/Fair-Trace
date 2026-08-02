import os
import asyncio
from typing import Dict, Any

class PipelineRunner:
    def __init__(self, api_client, auth_headers):
        self.api_client = api_client
        self.auth_headers = auth_headers
        
    def upload_document(self, filepath: str) -> str:
        with open(filepath, "rb") as f:
            files = {"file": (os.path.basename(filepath), f, "application/pdf")}
            res = self.api_client.post("/api/v1/uploads", files=files, headers=self.auth_headers)
        if res.status_code != 200:
            raise Exception(f"Upload failed: {res.text}")
        return res.json()["data"]["id"]
        
    def extract_document(self, document_id: str):
        res = self.api_client.post(f"/api/v1/uploads/{document_id}/parse", headers=self.auth_headers)
        if res.status_code != 200:
            raise Exception(f"Extract failed: {res.text}")
            
    def start_workflow(self, document_id: str) -> str:
        res = self.api_client.post("/api/v1/workflows/start", json={"document_id": document_id}, headers=self.auth_headers)
        if res.status_code != 200:
            raise Exception(f"Start workflow failed: {res.text}")
        return res.json()["workflow_id"]
        
    def get_workflow_state(self, workflow_id: str) -> Dict[str, Any]:
        res = self.api_client.get(f"/api/v1/workflows/{workflow_id}", headers=self.auth_headers)
        return res.json().get("state", {})
        
    def wait_for_status(self, workflow_id: str, expected_status: str, timeout: int = 30):
        import time
        for _ in range(timeout):
            res = self.api_client.get(f"/api/v1/workflows/{workflow_id}", headers=self.auth_headers)
            if res.status_code == 200 and res.json()["status"] == expected_status:
                return
            time.sleep(0.5)
        raise TimeoutError(f"Workflow {workflow_id} did not reach {expected_status}")
        
    def approve_workflow(self, workflow_id: str, notes: str):
        res = self.api_client.post(
            f"/api/v1/workflows/{workflow_id}/approve",
            json={"comments": notes, "decision": "APPROVED"},
            headers=self.auth_headers
        )
        if res.status_code != 200:
            raise Exception(f"Approve failed: {res.text}")
            
    def resume_workflow(self, workflow_id: str):
        res = self.api_client.post(f"/api/v1/workflows/{workflow_id}/resume", headers=self.auth_headers)
        if res.status_code != 200:
            raise Exception(f"Resume failed: {res.text}")
            
    def export_pdf(self, workflow_id: str) -> str:
        res = self.api_client.post(f"/api/v1/export/pdf/{workflow_id}", headers=self.auth_headers)
        if res.status_code != 200:
            raise Exception(f"Export failed: {res.text}")
        return res.json()["export_id"]
        
    def get_download_url(self, export_id: str) -> str:
        res = self.api_client.get(f"/api/v1/export/download/{export_id}", headers=self.auth_headers)
        return res.json()["download_url"]
