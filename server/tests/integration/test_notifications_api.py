"""
Notifications API integration tests.
Owner: Akash Pawar (PES2UG24CS041)
Sprint: S2 (S2-07)
Requirement IDs: TMA-F-040, TMA-F-041
"""

import pytest


class TestNotificationsApiLive:
    def test_list_notifications_unauthenticated_returns_401(self, client):
        """
        TC-Sec-01 | Owner: Akash | Requirement: TMA-SR-001 | Backlog: S2-07
        GET /api/notifications without auth returns 401.
        """
        response = client.get("/api/notifications")
        assert response.status_code == 401


class TestNotificationsApi:
    @pytest.mark.skip(reason="Pending implementation: S2-07")
    def test_list_notifications_authenticated(self, auth_client):
        """
        TC-Notify-01 | Owner: Akash | Requirement: TMA-F-040 | Backlog: S2-07
        GET /api/notifications returns user's notifications.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-07")
    def test_mark_notification_read(self, auth_client, db, test_user):
        """
        TC-Notify-01 | Owner: Akash | Requirement: TMA-F-041 | Backlog: S2-07
        PATCH /api/notifications/<id>/read marks notification as read.
        """
        pass

