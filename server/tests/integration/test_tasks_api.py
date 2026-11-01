"""
Tasks API integration tests.
Owner: Aadi Kore (PES2UG24CS006)
Sprint: S1 (S1-04, S1-05)
Requirement IDs: TMA-F-010, TMA-F-011, TMA-F-012
"""

import pytest


class TestTasksApiLive:
    """Live tests: unauthenticated access to task endpoints must return 401."""

    def test_list_tasks_unauthenticated_returns_401(self, client):
        """
        TC-Sec-01 | Owner: Aadi | Requirement: TMA-SR-001 | Backlog: S1-05
        GET /api/tasks without auth returns 401 (not 501 — auth check is live).
        """
        response = client.get("/api/tasks")
        assert response.status_code == 401
        data = response.get_json()
        assert data["success"] is False
        assert data["error"]["code"] == "AUTHENTICATION_ERROR"

    def test_create_task_unauthenticated_returns_401(self, client):
        """
        TC-Sec-01 | Owner: Aadi | Requirement: TMA-SR-001 | Backlog: S1-05
        POST /api/tasks without auth returns 401.
        """
        response = client.post("/api/tasks", json={"title": "Test"})
        assert response.status_code == 401

    def test_get_task_unauthenticated_returns_401(self, client):
        """TC-Sec-01 | Owner: Aadi | Requirement: TMA-SR-001 | Backlog: S1-05"""
        response = client.get("/api/tasks/1")
        assert response.status_code == 401


class TestTasksCrud:
    @pytest.mark.skip(reason="Pending implementation: S1-04")
    def test_create_task_authenticated(self, auth_client, test_user):
        """
        TC-Task-01 | Owner: Aadi | Requirement: TMA-F-010 | Backlog: S1-04
        POST /api/tasks creates a task for the authenticated user.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S1-04")
    def test_list_tasks_returns_only_owned(self, auth_client, test_user, test_admin, db):
        """
        TC-Task-01 | Owner: Aadi | Requirement: TMA-F-010 | Backlog: S1-04
        GET /api/tasks returns only current user's tasks.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S1-04")
    def test_update_own_task(self, auth_client, sample_task):
        """
        TC-Task-02 | Owner: Aadi | Requirement: TMA-F-011 | Backlog: S1-04
        PATCH /api/tasks/<id> updates owned task successfully.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S1-04")
    def test_update_another_users_task_returns_404(self, auth_client, db, test_admin):
        """
        TC-Sec-01 | Owner: Aadi | Requirement: TMA-SR-001 | Backlog: S1-04
        PATCH /api/tasks/<other_user_task_id> returns 404 to prevent enumeration.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S1-04")
    def test_delete_own_task(self, auth_client, sample_task):
        """
        TC-Task-03 | Owner: Aadi | Requirement: TMA-F-012 | Backlog: S1-04
        DELETE /api/tasks/<id> removes the owned task.
        """
        pass

