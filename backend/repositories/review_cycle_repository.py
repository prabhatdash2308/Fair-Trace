"""FairTrace — ReviewCycle Repository"""

from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from models.db.review_cycle import ReviewCycle
from models.enums import ReviewCycleStatus
from repositories.base_repository import BaseRepository


class ReviewCycleRepository(BaseRepository[ReviewCycle]):
    def __init__(self):
        super().__init__(ReviewCycle)

    def update_status(self, db: Session, cycle: ReviewCycle, status: ReviewCycleStatus) -> ReviewCycle:
        return self.update(db, cycle, {"status": status})


review_cycle_repo = ReviewCycleRepository()
