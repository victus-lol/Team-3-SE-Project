"""
Deterministic notification scheduler.
Owner: Akash Pawar (PES2UG24CS041)
Sprint: S2 (S2-07)

The project has not selected a production scheduler or default reminder time.
This component therefore exposes an explicit queue and run_pending() method.
The application/host decides when to call run_pending(); no thread or timer is
started implicitly. Tests can drive it with FakeNotificationProvider.
"""

from ..common.exceptions import NotFoundError, ValidationError
from ..common.responses import success_response
from .service import dispatch_notification


class NotificationScheduler:
    """Small manually-driven scheduler suitable for deterministic tests."""

    def __init__(self, provider):
        if provider is None or not callable(getattr(provider, "send", None)):
            raise ValueError("A notification provider with a send() method is required.")
        self.provider = provider
        self._running = False
        self._queue: list[int] = []

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def pending_ids(self) -> tuple[int, ...]:
        """Read-only snapshot of queued notification IDs."""
        return tuple(self._queue)

    def start(self):
        """Enable explicit run_pending() dispatch calls."""
        self._running = True
        return self

    def stop(self):
        """Disable dispatch without discarding queued reminders."""
        self._running = False

    def schedule_reminder(self, notification_id: int):
        """Queue a persisted notification once; its scheduled_at controls due time."""
        if (
            isinstance(notification_id, bool)
            or not isinstance(notification_id, int)
            or notification_id <= 0
        ):
            raise ValidationError("notification_id must be a positive integer.")
        if notification_id not in self._queue:
            self._queue.append(notification_id)
        return notification_id

    def run_pending(self, *, now=None) -> list:
        """
        Dispatch queued reminders that are due.

        This method is deliberately explicit rather than starting a background
        thread. Future reminders stay queued for the next host poll.
        """
        if not self._running:
            return []

        results = []
        remaining = []
        for notification_id in self._queue:
            try:
                notification = dispatch_notification(
                    notification_id,
                    self.provider,
                    now=now,
                )
            except NotFoundError:
                # A deleted notification should not poison the remaining queue.
                continue

            results.append(notification)
            if notification.status == "pending":
                remaining.append(notification_id)

        self._queue = remaining
        return results
