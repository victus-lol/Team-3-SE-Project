"""
Notifications API integration tests.
Owner: Akash Pawar (PES2UG24CS041)
Sprint: S2 (S2-07)
Requirement IDs: TMA-F-040, TMA-F-041
"""

from app.notifications.service import create_notification


class TestNotificationsApi:
    def test_list_notifications_unauthenticated_returns_401(self, client):
        """TC-Sec-01 | Requirement: TMA-SR-001 | Backlog: S2-07"""
        response = client.get("/api/notifications")
        assert response.status_code == 401

    def test_list_notifications_authenticated_and_user_scoped(
        self, auth_client, db, test_user, test_admin
    ):
        """TC-Notify-01 | Requirement: TMA-F-040 | Backlog: S2-07"""
        own = create_notification(test_user.id, "My reminder")
        create_notification(test_admin.id, "Private reminder")

        response = auth_client.get("/api/notifications")

        assert response.status_code == 200
        body = response.get_json()
        assert body["success"] is True
        assert [item["id"] for item in body["data"]] == [own.id]
        assert all(item["user_id"] == test_user.id for item in body["data"])

    def test_mark_notification_read(self, auth_client, db, test_user):
        """TC-Notify-01 | Requirement: TMA-F-041 | Backlog: S2-07"""
        notification = create_notification(test_user.id, "Please read")

        response = auth_client.patch(f"/api/notifications/{notification.id}/read")

        assert response.status_code == 200
        body = response.get_json()
        assert body["success"] is True
        assert body["data"]["status"] == "read"

    def test_cannot_mark_another_users_notification_read(self, auth_client, db, test_admin):
        """Foreign notification IDs must be hidden with 404."""
        notification = create_notification(test_admin.id, "Not yours")

        response = auth_client.patch(f"/api/notifications/{notification.id}/read")

        assert response.status_code == 404
