"""FairTrace — Centralized Action & Permission Constants"""

from enum import Enum

class ResourceAction(str, Enum):
    # People
    PEOPLE_CREATE = "people.create"
    PEOPLE_READ = "people.read"
    PEOPLE_UPDATE = "people.update"
    PEOPLE_DELETE = "people.delete"

    # Review Cycles
    REVIEW_CYCLE_CREATE = "review_cycle.create"
    REVIEW_CYCLE_READ = "review_cycle.read"
    REVIEW_CYCLE_UPDATE = "review_cycle.update"
    REVIEW_CYCLE_DELETE = "review_cycle.delete"

    # Reviews
    REVIEW_CREATE = "review.create"
    REVIEW_READ = "review.read"
    REVIEW_UPDATE = "review.update"
    REVIEW_APPROVE = "review.approve"
    REVIEW_DELETE = "review.delete"

    # Goals
    GOAL_CREATE = "goal.create"
    GOAL_READ = "goal.read"
    GOAL_UPDATE = "goal.update"
    GOAL_DELETE = "goal.delete"

    # Feedback
    FEEDBACK_CREATE = "feedback.create"
    FEEDBACK_READ = "feedback.read"
    FEEDBACK_UPDATE = "feedback.update"
    FEEDBACK_DELETE = "feedback.delete"

    # Reports
    REPORT_READ = "report.read"
    REPORT_APPROVE = "report.approve"
    REPORT_UPDATE = "report.update"

    # Insights
    INSIGHT_READ = "insight.read"
    INSIGHT_GENERATE = "insight.generate"
