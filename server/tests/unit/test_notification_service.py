"""
Notification service and scheduler unit tests.
Owner: Akash Pawar (PES2UG24CS041)
Sprint: S2 (S2-07)
Requirement IDs: TMA-F-040, TMA-F-041, TMA-F-042
"""

from datetime import datetime, timedelta, timezone

import pytest

from app.common.exceptions import NotFoundError, ValidationError
from app.models.notification import Notification
from app.notifications.scheduler import NotificationScheduler
from app.notifications.service import (
    create_notification,
    dispatch_notification,
    list_notifications,
    mark_notification_read,
)


class TestNotificationService:
    def test_create_notification(self, db, test_user):
        """TC-Notify-01 | Requirement: TMA-F-040 | Backlog: S2-07"""
        notification = create_notification(
            user_id=test_user.id,
            message="  Task is due soon.  ",
        )

        assert notification.id is not None
        assert notification.user_id == test_user.id
        assert notification.message == "Task is due soon."
        assert notification.status == "pending"

    def test_list_notifications_scoped_to_user(self, db, test_user, test_admin):
        """TC-Notify-01 | Requirement: TMA-F-040 | Backlog: S2-07"""
        own = create_notification(test_user.id, "My notification")
        create_notification(test_admin.id, "Other user's notification")

        results = list_notifications(test_user.id)

        assert [item.id for item in results] == [own.id]
        assert all(item.user_id == test_user.id for item in results)

    def test_mark_notification_read(self, db, test_user):
        """TC-Notify-01 | Requirement: TMA-F-041 | Backlog: S2-07"""
        notification = create_notification(test_user.id, "Read me")

        updated = mark_notification_read(notification.id, test_user.id)

        assert updated.status == "read"
        assert mark_notification_read(notification.id, test_user.id).status == "read"

    def test_cannot_mark_another_users_notification_read(self, db, test_user, test_admin):
        notification = create_notification(test_admin.id, "Private notification")

        with pytest.raises(NotFoundError):
            mark_notification_read(notification.id, test_user.id)

    def test_create_rejects_empty_or_oversized_message(self, db, test_user):
        with pytest.raises(ValidationError):
            create_notification(test_user.id, "   ")
        with pytest.raises(ValidationError):
            create_notification(test_user.id, "x" * 513)

    def test_create_rejects_task_owned_by_another_user(self, db, test_user, test_admin):
        from app.models.task import Task

        task = Task(owner_id=test_admin.id, title="Private task")
        db.session.add(task)
        db.session.commit()

        with pytest.raises(NotFoundError):
            create_notification(test_user.id, "Cannot reference foreign task", task_id=task.id)

    def test_scheduled_at_must_be_timezone_aware(self, db, test_user):
        with pytest.raises(ValidationError):
            create_notification(
                test_user.id,
                "Timezone required",
                scheduled_at=datetime(2026, 11, 3, 9, 0),
            )

    def test_dispatch_uses_provider_and_marks_delivered(self, db, test_user, fake_provider):
        notification = create_notification(test_user.id, "Delivery test")

        updated = dispatch_notification(notification.id, fake_provider)

        assert updated.status == "delivered"
        assert updated.delivered_at is not None
        assert fake_provider.last_sent()["message"] == "Delivery test"

    def test_future_notification_remains_pending(self, db, test_user, fake_provider):
        future = datetime.now(timezone.utc) + timedelta(days=1)
        notification = create_notification(
            test_user.id,
            "Not due yet",
            scheduled_at=future,
        )

        updated = dispatch_notification(
            notification.id,
            fake_provider,
            now=datetime.now(timezone.utc),
        )

        assert updated.status == "pending"
        assert fake_provider.sent == []

    def test_provider_failure_marks_notification_failed(self, db, test_user):
        class FailingProvider:
            def send(self, **kwargs):
                return False

        notification = create_notification(test_user.id, "Failure test")
        updated = dispatch_notification(notification.id, FailingProvider())

        assert updated.status == "failed"
        assert updated.delivered_at is None


class TestNotificationScheduler:
    def test_scheduler_requires_start_and_dispatches_queue(self, db, test_user, fake_provider):
        notification = create_notification(test_user.id, "Scheduled delivery")
        scheduler = NotificationScheduler(provider=fake_provider)
        scheduler.schedule_reminder(notification.id)

        assert scheduler.run_pending() == []
        assert scheduler.pending_ids == (notification.id,)

        scheduler.start()
        results = scheduler.run_pending()

        assert len(results) == 1
        assert results[0].status == "delivered"
        assert scheduler.pending_ids == ()

    def test_future_reminder_stays_queued_until_due(self, db, test_user, fake_provider):
        future = datetime.now(timezone.utc) + timedelta(days=1)
        notification = create_notification(
            test_user.id,
            "Future delivery",
            scheduled_at=future,
        )
        scheduler = NotificationScheduler(provider=fake_provider).start()
        scheduler.schedule_reminder(notification.id)

        scheduler.run_pending(now=datetime.now(timezone.utc))

        assert scheduler.pending_ids == (notification.id,)
        assert fake_provider.sent == []

    def test_scheduler_stop_preserves_queue(self, db, test_user, fake_provider):
        notification = create_notification(test_user.id, "Stopped scheduler")
        scheduler = NotificationScheduler(provider=fake_provider).start()
        scheduler.schedule_reminder(notification.id)
        scheduler.stop()

        assert scheduler.is_running is False
        assert scheduler.run_pending() == []
        assert scheduler.pending_ids == (notification.id,)
