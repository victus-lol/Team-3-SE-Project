"""
Dashboard summary API integration tests.
Owner: Balaji Gowda S R (PES2UG25CS804)
Sprint: S2 (S2-04)
Requirement IDs: TMA-F-033
"""

from app.models.task import Task


class TestDashboardApiLive:
    def test_summary_unauthenticated_returns_401(self, client):
        """
        TC-Sec-01 | Owner: Balaji | Requirement: TMA-SR-001 | Backlog: S2-04
        GET /api/dashboard/summary without auth returns 401.
        """
        response = client.get("/api/dashboard/summary")
        assert response.status_code == 401
        payload = response.get_json()
        assert payload["success"] is False
        assert payload["error"]["code"] == "AUTHENTICATION_ERROR"
        assert "message" in payload["error"]


class TestDashboardApi:
    def test_summary_returns_counts(self, auth_client, db, test_user):
        """
        TC-Summary-01 | Owner: Balaji | Requirement: TMA-F-033 | Backlog: S2-04
        GET /api/dashboard/summary returns pending/in_progress/completed counts in standard envelope.
        """
        tasks = [
            Task(owner_id=test_user.id, title="Task P1", status="pending"),
            Task(owner_id=test_user.id, title="Task P2", status="pending"),
            Task(owner_id=test_user.id, title="Task IP1", status="in_progress"),
            Task(owner_id=test_user.id, title="Task C1", status="completed"),
            Task(owner_id=test_user.id, title="Task C2", status="completed"),
            Task(owner_id=test_user.id, title="Task C3", status="completed"),
        ]
        db.session.add_all(tasks)
        db.session.commit()

        response = auth_client.get("/api/dashboard/summary")
        assert response.status_code == 200
        payload = response.get_json()
        assert payload["success"] is True
        assert payload["message"] == "Dashboard summary retrieved successfully."
        assert payload["data"] == {
            "pending": 2,
            "in_progress": 1,
            "completed": 3,
        }

    def test_summary_empty_dashboard(self, auth_client, db, test_user):
        """
        TC-Summary-01 | Owner: Balaji | Requirement: TMA-F-033 | Backlog: S2-04
        GET /api/dashboard/summary returns zero counts when user has no tasks.
        """
        response = auth_client.get("/api/dashboard/summary")
        assert response.status_code == 200
        payload = response.get_json()
        assert payload["success"] is True
        assert payload["message"] == "Dashboard summary retrieved successfully."
        assert payload["data"] == {
            "pending": 0,
            "in_progress": 0,
            "completed": 0,
        }

    def test_summary_scoped_to_user(self, auth_client, db, test_user, test_admin):
        """
        TC-Summary-01 | Owner: Balaji | Requirement: TMA-F-033 | Backlog: S2-04
        Dashboard counts reflect only the current user's tasks; other users' tasks are excluded.
        """
        user_tasks = [
            Task(owner_id=test_user.id, title="User Task 1", status="pending"),
            Task(owner_id=test_user.id, title="User Task 2", status="in_progress"),
            Task(owner_id=test_user.id, title="User Task 3", status="completed"),
        ]
        admin_tasks = [
            Task(owner_id=test_admin.id, title="Admin Task 1", status="pending"),
            Task(owner_id=test_admin.id, title="Admin Task 2", status="pending"),
            Task(owner_id=test_admin.id, title="Admin Task 3", status="in_progress"),
            Task(owner_id=test_admin.id, title="Admin Task 4", status="completed"),
        ]
        db.session.add_all(user_tasks + admin_tasks)
        db.session.commit()

        response = auth_client.get("/api/dashboard/summary")
        assert response.status_code == 200
        payload = response.get_json()
        assert payload["success"] is True
        assert payload["message"] == "Dashboard summary retrieved successfully."
        assert payload["data"] == {
            "pending": 1,
            "in_progress": 1,
            "completed": 1,
        }

