"""
Task business rules.
Owner: Aadi Kore (PES2UG24CS006)
Sprint: S2 (S2-01, S2-02)
"""

from datetime import date, datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from ..common.exceptions import ValidationError

VALID_PRIORITIES = {"low", "medium", "high"}
VALID_STATUSES = {"pending", "in_progress", "completed"}

SORTABLE_FIELDS = {
    "created_at",
    "updated_at",
    "due_date",
    "priority",
    "status",
    "title",
}

ALLOWED_STATUS_TRANSITIONS = {
    "pending": {"pending", "in_progress", "completed"},
    "in_progress": {"in_progress", "pending", "completed"},
    "completed": {"completed", "pending"},
}


def validate_priority(priority: str) -> None:
    if not isinstance(priority, str) or priority not in VALID_PRIORITIES:
        raise ValidationError("Priority must be one of: low, medium, high.")


def validate_status(status: str) -> None:
    if not isinstance(status, str) or status not in VALID_STATUSES:
        raise ValidationError("Status must be one of: pending, in_progress, completed.")


def validate_due_date(due_date_str: str | date | None) -> date | None:
    if due_date_str is None or due_date_str == "":
        return None

    if isinstance(due_date_str, datetime):
        raise ValidationError("Due date must use YYYY-MM-DD format.")

    if isinstance(due_date_str, date):
        return due_date_str

    if not isinstance(due_date_str, str):
        raise ValidationError("Due date must use YYYY-MM-DD format.")

    try:
        parsed = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValidationError("Due date must use YYYY-MM-DD format.") from exc

    if parsed.isoformat() != due_date_str:
        raise ValidationError("Due date must use YYYY-MM-DD format.")

    return parsed


def allowed_status_transitions(current: str, next_status: str) -> bool:
    if current not in VALID_STATUSES or next_status not in VALID_STATUSES:
        return False
    return next_status in ALLOWED_STATUS_TRANSITIONS[current]


def is_overdue(task, app_timezone: str = "UTC") -> bool:
    due_date = getattr(task, "due_date", None)
    status = getattr(task, "status", None)

    if due_date is None or status == "completed":
        return False

    try:
        today = datetime.now(ZoneInfo(app_timezone)).date()
    except ZoneInfoNotFoundError as exc:
        raise ValidationError("Invalid application timezone.") from exc

    if isinstance(due_date, datetime):
        due_date = due_date.date()

    return due_date < today
