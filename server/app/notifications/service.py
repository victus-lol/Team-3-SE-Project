"""
Notification service — reminder generation and delivery coordination.
Owner: Akash Pawar (PES2UG24CS041)
Sprint: S2 (S2-07)
Requirement IDs: TMA-F-040, TMA-F-041, TMA-F-042

TODO checklist:
  [ ] Implement list_notifications(user_id) → list[Notification]
  [ ] Implement mark_notification_read(notification_id, user_id) → Notification
  [ ] Implement create_notification(user_id, task_id, message, scheduled_at) → Notification
  [ ] Integrate with provider interface
  [ ] Write unit tests in tests/unit/test_notification_service.py
"""

from ..models.notification import Notification


def list_notifications(user_id: int) -> list:
    """TODO (S2-07 — Akash): Return all notifications for user_id."""
    raise NotImplementedError("list_notifications not implemented (S2-07)")


def mark_notification_read(notification_id: int, user_id: int) -> Notification:
    """TODO (S2-07 — Akash): Set notification status to 'read'. Verify ownership."""
    raise NotImplementedError("mark_notification_read not implemented (S2-07)")


def create_notification(
    user_id: int,
    message: str,
    task_id: int | None = None,
    scheduled_at=None,
) -> Notification:
    """TODO (S2-07 — Akash): Persist a new notification record."""
    raise NotImplementedError("create_notification not implemented (S2-07)")

