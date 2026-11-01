"""
Notification service unit tests.
Owner: Akash Pawar (PES2UG24CS041)
Sprint: S2 (S2-07)
Requirement IDs: TMA-F-040, TMA-F-041, TMA-F-042
"""

import pytest


class TestNotificationService:
    @pytest.mark.skip(reason="Pending implementation: S2-07")
    def test_create_notification(self, db, test_user):
        """
        TC-Notify-01 | Owner: Akash | Requirement: TMA-F-040 | Backlog: S2-07
        create_notification() persists a notification record.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-07")
    def test_list_notifications_scoped_to_user(self, db, test_user, test_admin):
        """
        TC-Notify-01 | Owner: Akash | Requirement: TMA-F-040 | Backlog: S2-07
        list_notifications() returns only the requesting user's notifications.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-07")
    def test_mark_notification_read(self, db, test_user):
        """
        TC-Notify-01 | Owner: Akash | Requirement: TMA-F-041 | Backlog: S2-07
        mark_notification_read() sets status to 'read'.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-07")
    def test_fake_provider_captures_sent(self, fake_provider):
        """
        TC-Notify-01 | Owner: Akash | Requirement: TMA-F-042 | Backlog: S2-07
        FakeNotificationProvider.send() captures message in sent list.
        """
        pass


class TestFakeProviderDirect:
    """These tests are LIVE — FakeNotificationProvider itself is implemented."""

    def test_fake_provider_send(self, fake_provider):
        """FakeNotificationProvider captures sent messages correctly."""
        fake_provider.send(user_id=1, message="Test notification", task_id=42)
        assert len(fake_provider.sent) == 1
        assert fake_provider.sent[0]["message"] == "Test notification"
        assert fake_provider.sent[0]["task_id"] == 42

    def test_fake_provider_clear(self, fake_provider):
        """clear() empties the sent list."""
        fake_provider.send(user_id=1, message="msg")
        fake_provider.clear()
        assert len(fake_provider.sent) == 0

    def test_fake_provider_last_sent(self, fake_provider):
        """last_sent() returns the most recent notification."""
        fake_provider.send(user_id=1, message="first")
        fake_provider.send(user_id=1, message="second")
        assert fake_provider.last_sent()["message"] == "second"

