"""FairTrace — Review Repository"""

from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload

from models.db.review import Review
from models.enums import ReviewStatus
from repositories.base_repository import BaseRepository


class ReviewRepository(BaseRepository[Review]):
    def __init__(self):
        super().__init__(Review)

    def get_with_relations(self, db: Session, review_id: UUID, organization_id: UUID | None = None) -> Review | None:
        stmt = (
            select(Review)
            .options(joinedload(Review.employee), joinedload(Review.manager))
            .where(Review.id == review_id)
        )
        if organization_id:
            stmt = stmt.where(Review.organization_id == organization_id)
        return db.scalar(stmt)

    def list_for_manager(self, db: Session, manager_id: UUID, skip: int = 0, limit: int = 20, organization_id: UUID | None = None):
        stmt = select(Review).where(Review.manager_id == manager_id)
        if organization_id:
            stmt = stmt.where(Review.organization_id == organization_id)
        total = db.scalar(select(func.count()).select_from(stmt.subquery()))
        items = db.scalars(stmt.offset(skip).limit(limit)).all()
        return list(items), total or 0

    def list_for_employee(self, db: Session, employee_id: UUID, skip: int = 0, limit: int = 20, organization_id: UUID | None = None):
        stmt = select(Review).where(Review.employee_id == employee_id)
        if organization_id:
            stmt = stmt.where(Review.organization_id == organization_id)
        total = db.scalar(select(func.count()).select_from(stmt.subquery()))
        items = db.scalars(stmt.offset(skip).limit(limit)).all()
        return list(items), total or 0

    def update_status(self, db: Session, review: Review, status: ReviewStatus) -> Review:
        return self.update(db, review, {"status": status})

    def has_active_pipeline(self, db: Session, review_id: UUID) -> bool:
        """Returns True if any report for this review is in a non-terminal pipeline state."""
        from models.db.report import Report
        from models.enums import ReportStatus
        count = db.scalar(
            select(func.count(Report.id)).where(
                Report.review_id == review_id,
                Report.status.in_([ReportStatus.DRAFT, ReportStatus.PENDING_APPROVAL]),
            )
        )
        return (count or 0) > 0


review_repo = ReviewRepository()
