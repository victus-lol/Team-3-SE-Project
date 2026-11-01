"""
Task service unit tests.
Owner: Aadi Kore (PES2UG24CS006)
Sprint: S1 (S1-04), S2 (S2-01)
Requirement IDs: TMA-F-010, TMA-F-011, TMA-F-012
"""

import pytest


class TestTaskService:
    """Unit tests for server/app/tasks/service.py"""

    @pytest.mark.skip(reason="Pending implementation: S1-04")
    def test_create_task_valid(self, db, test_user):
        """
        TC-Task-01 | Owner: Aadi | Requirement: TMA-F-010 | Backlog: S1-04
        create_task() persists and returns a Task with correct owner.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S1-04")
    def test_create_task_empty_title_rejected(self, db, test_user):
        """
        TC-Task-01 | Owner: Aadi | Requirement: TMA-F-010 | Backlog: S1-04
        create_task() raises ValidationError on empty title.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S1-04")
    def test_list_tasks_scoped_to_owner(self, db, test_user, test_admin):
        """
        TC-Task-01 | Owner: Aadi | Requirement: TMA-F-010 | Backlog: S1-04
        list_tasks() returns only the requesting user's tasks.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S1-04")
    def test_get_task_other_user_returns_404(self, db, test_user, test_admin, sample_task):
        """
        TC-Sec-01 | Owner: Aadi | Requirement: TMA-F-010 | Backlog: S1-04
        get_task_or_404() raises NotFoundError when accessed by non-owner.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S1-04")
    def test_update_task_owned(self, db, test_user, sample_task):
        """
        TC-Task-02 | Owner: Aadi | Requirement: TMA-F-011 | Backlog: S1-04
        update_task() modifies fields on an owned task.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S1-04")
    def test_delete_task_owned(self, db, test_user, sample_task):
        """
        TC-Task-03 | Owner: Aadi | Requirement: TMA-F-012 | Backlog: S1-04
        delete_task() removes the task from the database.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S1-04")
    def test_category_cross_user_rejected(self, db, test_user, test_admin):
        """
        TC-Org-04 | Owner: Aadi | Requirement: TMA-F-030 | Backlog: S1-04
        create_task() raises ValidationError when category belongs to different user.
        """
        pass

