"""ReviewGuard AI — ReviewInput, Report, BiasFlag, EvidenceCitation, AuditEvent Repositories"""

from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload

from models.db.review_input import ReviewInput
from models.db.report import Report
from models.db.bias_flag import BiasFlag
from models.db.evidence_citation import EvidenceCitation
from models.db.audit_event import AuditEvent
from models.enums import AuditEventType, UserRole
from repositories.base_repository import BaseRepository


# ── ReviewInput Repository ─────────────────────────────────────────────────────

class ReviewInputRepository(BaseRepository[ReviewInput]):
    def __init__(self):
        super().__init__(ReviewInput)

    def list_for_cycle(self, db: Session, cycle_id: UUID) -> list[ReviewInput]:
        return list(
            db.scalars(select(ReviewInput).where(ReviewInput.review_cycle_id == cycle_id)).all()
        )

    def count_for_cycle(self, db: Session, cycle_id: UUID) -> int:
        return db.scalar(
            select(func.count(ReviewInput.id)).where(ReviewInput.review_cycle_id == cycle_id)
        ) or 0

    def update_qdrant_id(self, db: Session, input_id: UUID, qdrant_doc_id: str) -> None:
        stmt = select(ReviewInput).where(ReviewInput.id == input_id)
        review_input = db.scalar(stmt)
        if review_input:
            review_input.qdrant_document_id = qdrant_doc_id
            db.flush()


review_input_repo = ReviewInputRepository()


# ── Report Repository ──────────────────────────────────────────────────────────

class ReportRepository(BaseRepository[Report]):
    def __init__(self):
        super().__init__(Report)

    def get_current_for_cycle(self, db: Session, cycle_id: UUID) -> Report | None:
        return db.scalar(
            select(Report)
            .options(
                joinedload(Report.claims).joinedload("citations"),
                joinedload(Report.bias_flags),
            )
            .where(Report.review_cycle_id == cycle_id, Report.is_current == True)
        )

    def get_with_full_details(self, db: Session, report_id: UUID) -> Report | None:
        return db.scalar(
            select(Report)
            .options(
                joinedload(Report.claims).joinedload("citations"),
                joinedload(Report.bias_flags),
                joinedload(Report.approver),
            )
            .where(Report.id == report_id)
        )

    def get_versions_for_cycle(self, db: Session, cycle_id: UUID) -> list[Report]:
        return list(
            db.scalars(
                select(Report)
                .where(Report.review_cycle_id == cycle_id)
                .order_by(Report.version.desc())
            ).all()
        )

    def get_by_idempotency_key(self, db: Session, key: str) -> Report | None:
        return db.scalar(
            select(Report).where(Report.approval_idempotency_key == key)
        )

    def mark_previous_not_current(self, db: Session, cycle_id: UUID) -> None:
        """Set is_current=False on all existing reports for a cycle (before inserting new version)."""
        reports = db.scalars(
            select(Report).where(Report.review_cycle_id == cycle_id, Report.is_current == True)
        ).all()
        for r in reports:
            r.is_current = False
        db.flush()


report_repo = ReportRepository()


# ── BiasFlag Repository ────────────────────────────────────────────────────────

class BiasFlagRepository(BaseRepository[BiasFlag]):
    def __init__(self):
        super().__init__(BiasFlag)

    def list_for_report(self, db: Session, report_id: UUID) -> list[BiasFlag]:
        return list(
            db.scalars(select(BiasFlag).where(BiasFlag.report_id == report_id)).all()
        )


bias_flag_repo = BiasFlagRepository()


# ── EvidenceCitation Repository ────────────────────────────────────────────────

class EvidenceCitationRepository(BaseRepository[EvidenceCitation]):
    def __init__(self):
        super().__init__(EvidenceCitation)

    def list_for_claim(self, db: Session, claim_id: UUID) -> list[EvidenceCitation]:
        return list(
            db.scalars(
                select(EvidenceCitation)
                .where(EvidenceCitation.claim_id == claim_id)
                .order_by(EvidenceCitation.retrieval_rank)
            ).all()
        )


citation_repo = EvidenceCitationRepository()


# ── AuditEvent Repository (write-only) ─────────────────────────────────────────

class AuditRepository:
    """
    Write-only repository. Explicitly does NOT inherit BaseRepository.
    No update() or delete() methods — audit events are immutable.
    """

    def create(self, db: Session, event_data: dict) -> AuditEvent:
        event = AuditEvent(**event_data)
        db.add(event)
        db.flush()
        return event

    def get_by_resource(
        self,
        db: Session,
        resource_type: str,
        resource_id: UUID,
        skip: int = 0,
        limit: int = 50,
    ) -> list[AuditEvent]:
        return list(
            db.scalars(
                select(AuditEvent)
                .where(
                    AuditEvent.resource_type == resource_type,
                    AuditEvent.resource_id == resource_id,
                )
                .order_by(AuditEvent.occurred_at.desc())
                .offset(skip)
                .limit(limit)
            ).all()
        )

    def get_for_pipeline(self, db: Session, pipeline_run_id: str) -> list[AuditEvent]:
        return list(
            db.scalars(
                select(AuditEvent)
                .where(AuditEvent.correlation_id == pipeline_run_id)
                .order_by(AuditEvent.occurred_at.asc())
            ).all()
        )

    def list_recent(self, db: Session, skip: int = 0, limit: int = 50) -> list[AuditEvent]:
        return list(
            db.scalars(
                select(AuditEvent).order_by(AuditEvent.occurred_at.desc()).offset(skip).limit(limit)
            ).all()
        )


audit_repo = AuditRepository()
