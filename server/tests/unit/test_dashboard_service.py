"""
Dashboard service unit tests.
Owner: Balaji Gowda S R (PES2UG25CS804)
Sprint: S2 (S2-04)
Requirement IDs: TMA-F-033
"""

from app.dashboard.service import get_summary
from app.models.task import Task


class TestDashboardService:
    def test_get_summary_all_statuses(self, db, test_user):
        """
        TC-Summary-01 | Owner: Balaji | Requirement: TMA-F-033 | Backlog: S2-04
        get_summary returns accurate counts for all task statuses.
        """
        tasks = [
            Task(owner_id=test_user.id, title="P1", status="pending"),
            Task(owner_id=test_user.id, title="IP1", status="in_progress"),
            Task(owner_id=test_user.id, title="IP2", status="in_progress"),
            Task(owner_id=test_user.id, title="C1", status="completed"),
        ]
        db.session.add_all(tasks)
        db.session.commit()

        counts = get_summary(test_user.id)
        assert counts == {
            "pending": 1,
            "in_progress": 2,
            "completed": 1,
        }

    def test_get_summary_empty(self, db, test_user):
        """
        TC-Summary-01 | Owner: Balaji | Requirement: TMA-F-033 | Backlog: S2-04
        get_summary returns zero counts when user has no tasks.
        """
        counts = get_summary(test_user.id)
        assert counts == {
            "pending": 0,
            "in_progress": 0,
            "completed": 0,
        }

    def test_get_summary_user_scoped(self, db, test_user, test_admin):
        """
        TC-Summary-01 | Owner: Balaji | Requirement: TMA-F-033 | Backlog: S2-04
        get_summary strictly scopes aggregation to the queried user_id.
        """
        user_tasks = [
            Task(owner_id=test_user.id, title="User Task", status="pending"),
        ]
        admin_tasks = [
            Task(owner_id=test_admin.id, title="Admin Task 1", status="pending"),
            Task(owner_id=test_admin.id, title="Admin Task 2", status="completed"),
        ]
        db.session.add_all(user_tasks + admin_tasks)
        db.session.commit()

        user_counts = get_summary(test_user.id)
        admin_counts = get_summary(test_admin.id)

        assert user_counts == {"pending": 1, "in_progress": 0, "completed": 0}
        assert admin_counts == {"pending": 1, "in_progress": 0, "completed": 1}

