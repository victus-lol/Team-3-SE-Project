"""
Task business rules unit tests.
Owner: Aadi Kore (PES2UG24CS006)
Sprint: S2 (S2-01, S2-02)
Requirement IDs: TMA-F-020, TMA-F-021, TMA-F-022
"""

import pytest


class TestPriorityRules:
    @pytest.mark.skip(reason="Pending implementation: S2-01")
    def test_valid_priorities_accepted(self):
        """
        TC-Org-01 | Owner: Aadi | Requirement: TMA-F-020 | Backlog: S2-01
        validate_priority() accepts low/medium/high without raising.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-01")
    def test_invalid_priority_raises_error(self):
        """
        TC-Org-01 | Owner: Aadi | Requirement: TMA-F-020 | Backlog: S2-01
        validate_priority() raises ValidationError on 'urgent' or other invalid value.
        """
        pass


class TestDueDateRules:
    @pytest.mark.skip(reason="Pending implementation: S2-01")
    def test_valid_date_string_parsed(self):
        """
        TC-Org-02 | Owner: Aadi | Requirement: TMA-F-020 | Backlog: S2-01
        validate_due_date('2025-12-31') returns a date object.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-01")
    def test_invalid_date_string_raises(self):
        """
        TC-Org-02 | Owner: Aadi | Requirement: TMA-F-020 | Backlog: S2-01
        validate_due_date('not-a-date') raises ValidationError.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-01")
    def test_none_due_date_returns_none(self):
        """
        TC-Org-02 | Owner: Aadi | Requirement: TMA-F-020 | Backlog: S2-01
        validate_due_date(None) returns None (optional field).
        """
        pass


class TestStatusRules:
    @pytest.mark.skip(reason="Pending implementation: S2-01")
    def test_valid_statuses_accepted(self):
        """
        TC-Org-03 | Owner: Aadi | Requirement: TMA-F-020 | Backlog: S2-01
        validate_status() accepts pending/in_progress/completed.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-01")
    def test_invalid_status_raises(self):
        """
        TC-Org-03 | Owner: Aadi | Requirement: TMA-F-020 | Backlog: S2-01
        validate_status('done') raises ValidationError.
        """
        pass


class TestOverdueRule:
    @pytest.mark.skip(reason="Pending implementation: S2-02")
    def test_past_due_date_is_overdue(self):
        """
        TC-Monitor-01 | Owner: Aadi | Requirement: TMA-F-022 | Backlog: S2-02
        A task due yesterday is overdue.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-02")
    def test_today_due_date_is_not_overdue(self):
        """
        TC-Monitor-01 | Owner: Aadi | Requirement: TMA-F-022 | Backlog: S2-02
        BOUNDARY: A task due TODAY is NOT overdue.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-02")
    def test_completed_task_not_overdue(self):
        """
        TC-Monitor-01 | Owner: Aadi | Requirement: TMA-F-022 | Backlog: S2-02
        A completed task is never overdue regardless of due date.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-02")
    def test_no_due_date_not_overdue(self):
        """
        TC-Monitor-01 | Owner: Aadi | Requirement: TMA-F-022 | Backlog: S2-02
        A task without a due_date is never overdue.
        """
        pass

