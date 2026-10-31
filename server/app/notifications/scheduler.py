"""
Notification scheduler skeleton.
Owner: Akash Pawar (PES2UG24CS041)
Sprint: S2 (S2-07)

OPEN DECISION: The reminder schedule and delivery mechanism are not yet decided.
See DECISIONS_AND_OPEN_QUESTIONS.md item (3).
No timing is invented here. No external service or account is required.

TODO checklist:
  [ ] Define scheduler interface (start, stop, schedule_reminder)
  [ ] Implement polling or event-based reminder dispatch using the provider
  [ ] Ensure scheduler uses fake provider in test environment
"""


class NotificationScheduler:
    """
    TODO (S2-07 — Akash): Scheduler for queued/pending notification delivery.
    Interface is defined here; implementation deferred to S2.
    """

    def __init__(self, provider=None):
        self.provider = provider

    def start(self):
        """TODO: Start the scheduling loop."""
        raise NotImplementedError("Scheduler not implemented (S2-07)")

    def stop(self):
        """TODO: Stop the scheduling loop."""
        raise NotImplementedError("Scheduler not implemented (S2-07)")

    def schedule_reminder(self, notification_id: int):
        """TODO: Enqueue a notification for delivery."""
        raise NotImplementedError("Scheduler not implemented (S2-07)")

