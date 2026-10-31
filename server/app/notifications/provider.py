"""
Notification provider interface + fake provider for tests.
Owner: Akash Pawar (PES2UG24CS041)
Sprint: S2 (S2-07)
Requirement IDs: TMA-F-042

No external account or service required.
FakeNotificationProvider is used in all tests.

TODO checklist:
  [ ] Define BaseProvider interface
  [ ] Implement FakeNotificationProvider (captures sent messages in-memory)
  [ ] Add RealProvider stub for future integration
"""


class BaseNotificationProvider:
    """Abstract provider interface. Concrete providers must implement send()."""

    def send(self, user_id: int, message: str, task_id: int | None = None) -> bool:
        """Send a notification. Return True on success."""
        raise NotImplementedError("Provider.send() must be implemented.")


class FakeNotificationProvider(BaseNotificationProvider):
    """
    In-memory fake provider for tests.
    Captures all sent notifications so tests can assert on them.
    """

    def __init__(self):
        self.sent: list[dict] = []

    def send(self, user_id: int, message: str, task_id: int | None = None) -> bool:
        self.sent.append({"user_id": user_id, "message": message, "task_id": task_id})
        return True

    def clear(self):
        self.sent.clear()

    def last_sent(self) -> dict | None:
        return self.sent[-1] if self.sent else None

