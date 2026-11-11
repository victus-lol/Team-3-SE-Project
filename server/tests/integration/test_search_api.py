"""
Search API integration tests.
Owner: Aadi Kore (PES2UG24CS006)
"""

from datetime import date, timedelta

from app.models.task import Task


class TestSearchApi:

    def test_search_by_keyword(self, auth_client, sample_task):
        response = auth_client.get(
            "/api/tasks?q=Sample"
        )

        assert response.status_code == 200
        data = response.get_json()["data"]
        assert any(task["id"] == sample_task.id for task in data)

    def test_filter_by_status(self, auth_client, db, test_user):
        db.session.add(Task(
            owner_id=test_user.id,
            title="Pending task",
            status="pending",
        ))
        db.session.add(Task(
            owner_id=test_user.id,
            title="Completed task",
            status="completed",
        ))
        db.session.commit()

        response = auth_client.get(
            "/api/tasks?status=pending"
        )

        assert response.status_code == 200
        data = response.get_json()["data"]
        assert all(task["status"] == "pending" for task in data)

    def test_sort_by_created_at(self, auth_client, db, test_user):
        db.session.add(Task(
            owner_id=test_user.id,
            title="First",
        ))
        db.session.add(Task(
            owner_id=test_user.id,
            title="Second",
        ))
        db.session.commit()

        response = auth_client.get(
            "/api/tasks?sort_by=created_at&order=asc"
        )

        assert response.status_code == 200
        data = response.get_json()["data"]
        assert len(data) == 2

    def test_invalid_sort_field_rejected(self, auth_client):
        response = auth_client.get(
            "/api/tasks?sort_by=injected_column"
        )

        assert response.status_code == 400