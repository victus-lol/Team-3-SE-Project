"""
Task service — business logic for task CRUD.
Owner: Aadi Kore (PES2UG24CS006)
Sprint: S1 (S1-04, S1-05), S2 (S2-01, S2-02)
Requirement IDs: TMA-F-010, TMA-F-011, TMA-F-012

TODO checklist:
  [ ] Implement get_tasks_for_user(user_id, filters) → list[Task]
  [ ] Implement create_task(owner_id, data) → Task
  [ ] Implement get_task(task_id, user_id) → Task (404 if not owned)
  [ ] Implement update_task(task_id, user_id, data) → Task
  [ ] Implement delete_task(task_id, user_id) → None
  [ ] Validate category ownership before assigning (no cross-user categories)
  [ ] Apply rules from rules.py for priority, status, due_date
  [ ] Write unit tests in tests/unit/test_task_service.py
"""

from ..models.task import Task


def get_task_or_404(task_id: int, user_id: int) -> Task:
    """
    TODO (S1-04 — Aadi): Return task if owned by user_id, else raise NotFoundError.
    Returns 404 (not 403) to prevent enumeration — see DECISIONS_AND_OPEN_QUESTIONS.md.
    """
    raise NotImplementedError("get_task_or_404 not implemented (S1-04)")


def list_tasks(user_id: int, filters: dict | None = None) -> list:
    """
    TODO (S1-04 — Aadi): Return all tasks for user_id matching filters.
    Results must always be scoped to user_id.
    """
    raise NotImplementedError("list_tasks not implemented (S1-04)")


def create_task(owner_id: int, data: dict) -> Task:
    """TODO (S1-04 — Aadi): Create and persist a task."""
    raise NotImplementedError("create_task not implemented (S1-04)")


def update_task(task_id: int, user_id: int, data: dict) -> Task:
    """TODO (S1-04 — Aadi): Update fields on an owned task."""
    raise NotImplementedError("update_task not implemented (S1-04)")


def delete_task(task_id: int, user_id: int) -> None:
    """TODO (S1-04 — Aadi): Delete an owned task."""
    raise NotImplementedError("delete_task not implemented (S1-04)")

