"""
Dashboard service.
Owner: Balaji Gowda S R (PES2UG25CS804)
Sprint: S2 (S2-04)
Requirement IDs: TMA-F-033

TODO checklist:
  [x] Implement get_summary(user_id) → dict with pending/in_progress/completed counts
  [x] Counts must be scoped to user_id only
  [x] Write integration tests in tests/integration/test_summary_api.py
"""

from sqlalchemy import func

from ..extensions import db
from ..models.task import Task


def get_summary(user_id: int) -> dict:
    """
    Query task counts grouped by status for user_id.
    TC-Summary-01 | Requirement: TMA-F-033 | Backlog: S2-04
    """
    counts = {
        "pending": 0,
        "in_progress": 0,
        "completed": 0,
    }

    results = (
        db.session.query(Task.status, func.count(Task.id))
        .filter(Task.owner_id == user_id)
        .group_by(Task.status)
        .all()
    )

    for status, count in results:
        if status in counts:
            counts[status] = count

    return counts
