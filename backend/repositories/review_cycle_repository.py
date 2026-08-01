"""ReviewGuard AI — ReviewCycle Repository"""

from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload

from models.db.review_cycle import ReviewCycle
from models.enums import ReviewCycleStatus
from repositories.base_repository import BaseRepository


class ReviewCycleRepository(BaseRepository[ReviewCycle]):
    def __init__(self):
        super().__init__(ReviewCycle)

    def get_with_relations(self, db: Session, cycle_id: UUID) -> ReviewCycle | None:
        return db.scalar(
            select(ReviewCycle)
            .options(joinedload(ReviewCycle.employee), joinedload(ReviewCycle.manager))
            .where(ReviewCycle.id == cycle_id)
        )

    def list_for_manager(self, db: Session, manager_id: UUID, skip: int = 0, limit: int = 20):
        stmt = select(ReviewCycle).where(ReviewCycle.manager_id == manager_id)
        total = db.scalar(select(func.count()).select_from(stmt.subquery()))
        items = db.scalars(stmt.offset(skip).limit(limit)).all()
        return list(items), total or 0

    def list_for_employee(self, db: Session, employee_id: UUID, skip: int = 0, limit: int = 20):
        stmt = select(ReviewCycle).where(ReviewCycle.employee_id == employee_id)
        total = db.scalar(select(func.count()).select_from(stmt.subquery()))
        items = db.scalars(stmt.offset(skip).limit(limit)).all()
        return list(items), total or 0

    def update_status(self, db: Session, cycle: ReviewCycle, status: ReviewCycleStatus) -> ReviewCycle:
        return self.update(db, cycle, {"status": status})

    def has_active_pipeline(self, db: Session, cycle_id: UUID) -> bool:
        """Returns True if any report for this cycle is in a non-terminal pipeline state."""
        from models.db.report import Report
        from models.enums import ReportStatus
        count = db.scalar(
            select(func.count(Report.id)).where(
                Report.review_cycle_id == cycle_id,
                Report.status.in_([ReportStatus.DRAFT, ReportStatus.PENDING_APPROVAL]),
            )
        )
        return (count or 0) > 0


review_cycle_repo = ReviewCycleRepository()
