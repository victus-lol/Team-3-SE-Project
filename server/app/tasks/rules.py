"""
Task business rules — pure functions, no DB access.
Owner: Aadi Kore (PES2UG24CS006)
Sprint: S2 (S2-01)
Requirement IDs: TMA-F-020, TMA-F-021

Rules live here, not in service.py, so they can be unit-tested independently.

TODO checklist (S2-01):
  [ ] Implement validate_priority(priority) → raises ValidationError
  [ ] Implement validate_status(status) → raises ValidationError
  [ ] Implement validate_due_date(due_date_str) → raises ValidationError
  [ ] Implement is_overdue(task) → bool (uses APP_TIMEZONE; boundary: today is NOT overdue)
  [ ] Implement allowed_status_transitions(current, next) → bool
  [ ] Write unit tests in tests/unit/test_task_rules.py (TC-Org-01..04, TC-Monitor-01)
"""

import datetime

VALID_PRIORITIES = {"low", "medium", "high"}
VALID_STATUSES = {"pending", "in_progress", "completed"}

# Allowed field names for sort_by (allowlist — never interpolate raw column names)
SORTABLE_FIELDS = {"created_at", "updated_at", "due_date", "priority", "status", "title"}


def validate_priority(priority: str) -> None:
    """
    TODO (S2-01 — Aadi): Raise ValidationError if priority not in VALID_PRIORITIES.
    TC-Org-01 | Requirement: TMA-F-020 | Backlog: S2-01
    """
    raise NotImplementedError("validate_priority not implemented (S2-01)")


def validate_status(status: str) -> None:
    """
    TODO (S2-01 — Aadi): Raise ValidationError if status not in VALID_STATUSES.
    TC-Org-03 | Requirement: TMA-F-020 | Backlog: S2-01
    """
    raise NotImplementedError("validate_status not implemented (S2-01)")


def validate_due_date(due_date_str: str | None) -> datetime.date | None:
    """
    TODO (S2-01 — Aadi): Parse 'YYYY-MM-DD' string; return date or None.
    Raise ValidationError on invalid format.
    TC-Org-02 | Requirement: TMA-F-020 | Backlog: S2-01
    """
    raise NotImplementedError("validate_due_date not implemented (S2-01)")


def is_overdue(task, app_timezone: str = "UTC") -> bool:
    """
    TODO (S2-02 — Aadi): Return True if task is incomplete AND due_date < today in app_timezone.
    A task due TODAY is NOT overdue (boundary rule).
    TC-Monitor-01 | Requirement: TMA-F-022 | Backlog: S2-02
    """
    raise NotImplementedError("is_overdue not implemented (S2-02)")

