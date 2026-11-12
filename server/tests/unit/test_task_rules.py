from datetime import date, timedelta
from types import SimpleNamespace

import pytest

from app.common.exceptions import ValidationError
from app.tasks.rules import (
    allowed_status_transitions,
    is_overdue,
    validate_due_date,
    validate_priority,
    validate_status,
)


@pytest.mark.parametrize("priority", ["low", "medium", "high"])
def test_valid_priorities(priority):
    assert validate_priority(priority) is None


@pytest.mark.parametrize("priority", ["urgent", "", None, "LOW"])
def test_invalid_priorities(priority):
    with pytest.raises(ValidationError):
        validate_priority(priority)


@pytest.mark.parametrize("status", ["pending", "in_progress", "completed"])
def test_valid_statuses(status):
    assert validate_status(status) is None


@pytest.mark.parametrize("status", ["done", "cancelled", "", None])
def test_invalid_statuses(status):
    with pytest.raises(ValidationError):
        validate_status(status)


def test_valid_due_date():
    assert validate_due_date("2025-12-31") == date(2025, 12, 31)


def test_none_due_date():
    assert validate_due_date(None) is None


@pytest.mark.parametrize("value", ["not-a-date", "2025-02-30", "31-12-2025"])
def test_invalid_due_date(value):
    with pytest.raises(ValidationError):
        validate_due_date(value)


def test_due_date_today_is_not_overdue():
    task = SimpleNamespace(due_date=date.today(), status="pending")
    assert is_overdue(task) is False


def test_past_due_date_is_overdue():
    task = SimpleNamespace(
        due_date=date.today() - timedelta(days=2),
        status="pending",
    )
    assert is_overdue(task) is True


def test_completed_task_is_not_overdue():
    task = SimpleNamespace(
        due_date=date.today() - timedelta(days=1),
        status="completed",
    )
    assert is_overdue(task) is False


def test_task_without_due_date_is_not_overdue():
    task = SimpleNamespace(due_date=None, status="pending")
    assert is_overdue(task) is False


def test_allowed_status_transitions():
    assert allowed_status_transitions("pending", "in_progress")
    assert allowed_status_transitions("in_progress", "completed")
    assert not allowed_status_transitions("completed", "in_progress")
