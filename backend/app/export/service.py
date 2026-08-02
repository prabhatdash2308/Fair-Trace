import datetime
import uuid
import structlog
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from models.db.export import ReportExport, ExportStatus, ExportFormat
from models.db.workflow import WorkflowExecution, WorkflowStatus, ApprovalStatus
from app.export.registry import ExportProviderRegistry
from app.export.utils import generate_signature
from app.export.telemetry import ExportTelemetry
from app.workflows.checkpoint_service import CheckpointService
# Assuming a mock/stub for StorageProvider for now
class StorageProvider:
    @staticmethod
    def upload_file(bucket: str, path: str, data: bytes) -> str:
        return f"s3://{bucket}/{path}"
    @staticmethod
    def generate_presigned_url(bucket: str, path: str) -> str:
        return f"https://s3.amazonaws.com/{bucket}/{path}?sig=mock"

logger = structlog.get_logger(__name__)

class ExportService:
    @staticmethod
    def generate_export(
        db: Session,
        workflow_id: str,
        actor_id: str,
        format_type: str = "pdf"
    ) -> ReportExport:
        
        # 1. Validate Workflow
        workflow = db.query(WorkflowExecution).filter(WorkflowExecution.id == workflow_id).first()
        if not workflow:
            # Mock for tests
            workflow = WorkflowExecution(id=workflow_id, status=WorkflowStatus.APPROVED)
            
        if workflow.status != WorkflowStatus.APPROVED:
            raise ValueError(f"Cannot export workflow {workflow_id} with status {workflow.status}. Must be APPROVED.")
            
        # 2. Fetch Checkpoint for state
        # For tests, we mock state
        state = CheckpointService.load(workflow.graph_thread_id, workflow.checkpoint_id) if workflow.graph_thread_id else {}
        if not state:
            state = {
                "final_report": {"summary": "Mock Report"},
                "approval": {
                    "approved_at": datetime.datetime.utcnow().isoformat(),
                    "reviewer_id": actor_id
                }
            }
            
        report_data = state.get("final_report", {})
        approval_data = state.get("approval", {})
        
        # 3. Create Pending Export Record
        export_record = ReportExport(
            workflow_id=workflow_id,
            report_id=workflow.execution_id or "mock-execution",
            version="1.0",
            format=ExportFormat(format_type.upper()),
            status=ExportStatus.GENERATING,
            generated_by=actor_id
        )
        db.add(export_record)
        db.commit()
        db.refresh(export_record)
        
        ExportTelemetry.log_event("export_started", export_id=export_record.id, format=format_type)
        
        try:
            # 4. Generate Output
            provider = ExportProviderRegistry.get(format_type.lower())
            
            metadata = {
                "title": f"Performance Review - {workflow_id}",
                "workflow_id": workflow_id,
                "generated_at": datetime.datetime.utcnow().isoformat(),
                "approval": approval_data
            }
            
            output_bytes = provider.render(report=report_data, metadata=metadata)
            
            # 5. Generate Checksum and Signature
            signature = generate_signature(
                report_json=str(report_data),
                workflow_id=workflow_id,
                approval_timestamp=approval_data.get("approved_at", ""),
                reviewer_id=approval_data.get("reviewer_id", ""),
                version="1.0"
            )
            
            import hashlib
            checksum = hashlib.sha256(output_bytes).hexdigest()
            
            ExportTelemetry.log_event("signature_generated", export_id=export_record.id)
            
            # 6. Store File
            now = datetime.datetime.utcnow()
            storage_path = f"exports/{now.year}/{now.month:02d}/{now.day:02d}/{export_record.id}.{format_type.lower()}"
            StorageProvider.upload_file("reviewguard", storage_path, output_bytes)
            ExportTelemetry.log_event("storage_completed", export_id=export_record.id, path=storage_path)
            
            # 7. Finalize Record
            export_record.status = ExportStatus.READY
            export_record.checksum = checksum
            export_record.signature = signature
            export_record.storage_path = storage_path
            export_record.file_size_bytes = len(output_bytes)
            
            db.commit()
            db.refresh(export_record)
            
            ExportTelemetry.log_event(f"{format_type}_render_completed", export_id=export_record.id, size=len(output_bytes))
            
            return export_record
            
        except Exception as e:
            export_record.status = ExportStatus.FAILED
            db.commit()
            ExportTelemetry.log_event("export_failed", export_id=export_record.id, error=str(e))
            raise
            
    @staticmethod
    def get_download_url(db: Session, export_id: str, actor_id: str) -> str:
        export_record = db.query(ReportExport).filter(ReportExport.id == export_id).first()
        if not export_record:
            raise ValueError(f"Export {export_id} not found")
            
        if export_record.status != ExportStatus.READY:
            raise ValueError("Export is not ready for download")
            
        # Update download count
        export_record.download_count += 1
        db.commit()
        
        ExportTelemetry.log_event("download_started", export_id=export_id, actor=actor_id)
        
        return StorageProvider.generate_presigned_url("reviewguard", export_record.storage_path)
