"""Repository package — export all singletons for easy import."""
from repositories.base_repository import BaseRepository
from repositories.user_repository import user_repo
from repositories.review_cycle_repository import review_cycle_repo
from repositories.repositories import (
    review_input_repo,
    report_repo,
    bias_flag_repo,
    citation_repo,
    audit_repo,
)

__all__ = [
    "BaseRepository",
    "user_repo",
    "review_cycle_repo",
    "review_input_repo",
    "report_repo",
    "bias_flag_repo",
    "citation_repo",
    "audit_repo",
]
