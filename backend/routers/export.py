import uuid
import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Dict, Any

from dependencies import get_current_user, get_db
from models.db.user import User
from app.export.service import ExportService

router = APIRouter(prefix="/export", tags=["Export"])


def _report_to_render_dict(report) -> Dict[str, Any]:
    """Convert a Report ORM object to the dict expected by export providers."""
    competencies = {}
    for claim in (report.claims or []):
        if claim.dimension:
            competencies[claim.dimension.value] = claim.claim_text

    bias_flags = [
        {
            "bias_type": str(flag.bias_type.value) if flag.bias_type else "",
            "severity": str(flag.severity.value) if flag.severity else "",
            "recommended_action": flag.recommended_action or "",
            "detection_reasoning": flag.detection_reasoning or "",
        }
        for flag in (report.bias_flags or [])
    ]

    return {
        "summary": report.executive_summary or "",
        "recommended_actions": report.recommended_actions or [],
        "competencies": competencies,
        "bias_flags": bias_flags,
        "confidence_score": report.confidence_score.value if report.confidence_score else "",
        "confidence_explanation": report.confidence_explanation or "",
        "generated_at": report.generated_at.isoformat() if report.generated_at else "",
        "version": report.version,
    }


# -- New direct report export endpoints --

@router.get("/report/{report_id}/pdf", summary="Download Report as PDF")
async def download_report_pdf(
    report_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Streams a real PDF of the specified report.
    - ADMIN sees all reports in their organization.
    - MANAGER can only export reports for reviews they manage.
    - EMPLOYEE can only export their own FINALIZED reports.
    """
    from models.db.report import Report
    from models.enums import ReportStatus, UserRole

    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail=f"Report {report_id} not found.")

    # The report's organization is resolved through its review
    review = report.review
    if review is None:
        raise HTTPException(status_code=404, detail=f"Report {report_id} not found.")

    # Hard tenant isolation boundary — compare via the review's organization_id
    report_org_id = review.organization_id
    user_org_id = current_user.organization_id
    if report_org_id is None or str(report_org_id) != str(user_org_id):
        raise HTTPException(status_code=403, detail="Cross-organization export is not allowed.")

    _ADMIN_ROLES = (UserRole.ORG_ADMIN, UserRole.SUPER_ADMIN, UserRole.HR_ADMIN)
    if current_user.role == UserRole.MANAGER:
        if str(review.manager_id) != str(current_user.id):
            raise HTTPException(status_code=403, detail="You can only export reports for your own reviews.")
    elif current_user.role == UserRole.EMPLOYEE:
        if str(review.employee_id) != str(current_user.id):
            raise HTTPException(status_code=403, detail="You can only export your own reports.")
        if report.status != ReportStatus.FINALIZED:
            raise HTTPException(status_code=403, detail="Report is not yet finalized.")
    elif current_user.role not in _ADMIN_ROLES:
        raise HTTPException(status_code=403, detail="Access denied.")

    from app.export.providers.pdf_provider import PDFProvider

    report_data = _report_to_render_dict(report)
    metadata = {
        "title": f"FairTrace Performance Review - {review.title}",
        "report_id": str(report_id),
        "generated_at": datetime.datetime.utcnow().isoformat(),
    }

    try:
        provider = PDFProvider()
        pdf_bytes = provider.render(report=report_data, metadata=metadata)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"PDF rendering failed: {exc}")

    filename = f"fairtrace_report_{report_id}.pdf"
    return StreamingResponse(
        iter([pdf_bytes]),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/report/{report_id}/html", summary="Download Report as HTML")
async def download_report_html(
    report_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Streams an HTML version of the report (MANAGER/ADMIN only)."""
    from models.db.report import Report
    from models.enums import UserRole

    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail=f"Report {report_id} not found.")

    # The report's organization is resolved through its review
    review = report.review
    if review is None:
        raise HTTPException(status_code=404, detail=f"Report {report_id} not found.")

    # Hard tenant isolation boundary
    report_org_id = review.organization_id
    user_org_id = current_user.organization_id
    if report_org_id is None or str(report_org_id) != str(user_org_id):
        raise HTTPException(status_code=403, detail="Cross-organization export is not allowed.")

    _ADMIN_ROLES = (UserRole.ORG_ADMIN, UserRole.SUPER_ADMIN, UserRole.HR_ADMIN)
    if current_user.role == UserRole.EMPLOYEE:
        raise HTTPException(status_code=403, detail="HTML export is not available for employees.")
    elif current_user.role == UserRole.MANAGER:
        if str(review.manager_id) != str(current_user.id):
            raise HTTPException(status_code=403, detail="You can only export reports for your own reviews.")
    elif current_user.role not in _ADMIN_ROLES:
        raise HTTPException(status_code=403, detail="Access denied.")

    from app.export.providers.html_provider import HTMLProvider

    report_data = _report_to_render_dict(report)
    metadata = {
        "title": f"FairTrace Performance Review - {review.title}",
        "report_id": str(report_id),
        "generated_at": datetime.datetime.utcnow().isoformat(),
    }

    try:
        provider = HTMLProvider()
        html_bytes = provider.render(report=report_data, metadata=metadata)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"HTML rendering failed: {exc}")

    filename = f"fairtrace_report_{report_id}.html"
    return StreamingResponse(
        iter([html_bytes]),
        media_type="text/html",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# -- Legacy workflow-based export (preserved for compatibility) --

@router.post("/{format_type}/{workflow_id}", summary="[Legacy] Start Workflow Export")
async def start_export(
    format_type: str,
    workflow_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if format_type not in ["pdf", "html"]:
        raise HTTPException(status_code=400, detail="Invalid export format. Use 'pdf' or 'html'.")

    try:
        export_record = ExportService.generate_export(
            db=db,
            workflow_id=workflow_id,
            actor_id=current_user.id,
            format_type=format_type
        )
        return {"status": "success", "export_id": export_record.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Export rendering failed")


@router.get("/download/{export_id}", summary="[Legacy] Download Workflow Export")
async def download_export(
    export_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        url = ExportService.get_download_url(db=db, export_id=export_id, actor_id=current_user.id)
        return {"download_url": url}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/history", summary="Export History")
async def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return []


@router.get("/health", summary="Export Health Check")
async def export_health():
    return {"status": "healthy"}
