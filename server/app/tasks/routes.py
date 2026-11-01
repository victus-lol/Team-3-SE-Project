"""
Task routes.
Owner: Aadi Kore (PES2UG24CS006)
Sprint: S1 (S1-04, S1-05), S2 (S2-01, S2-02)
Requirement IDs: TMA-F-010, TMA-F-011, TMA-F-012, TMA-F-020, TMA-F-021

Endpoints:
  GET    /api/tasks           → list user's tasks (with search/filter params)
  POST   /api/tasks           → create a task
  GET    /api/tasks/<task_id> → get a single task
  PATCH  /api/tasks/<task_id> → update a task
  DELETE /api/tasks/<task_id> → delete a task

Search/filter query params (GET /api/tasks):
  q, status, priority, category_id, due_date_from, due_date_to, overdue,
  sort_by, order

TODO checklist (S1-04, S1-05):
  [ ] Implement list tasks (paginated, filtered by current user)
  [ ] Implement create task with full validation via schemas.py
  [ ] Implement get task — return 404 if not owned
  [ ] Implement update task — ownership enforced server-side
  [ ] Implement delete task — ownership enforced server-side
  [ ] Validate priority, status, due_date via rules.py
  [ ] Write integration tests in tests/integration/test_tasks_api.py
"""

from flask import Blueprint, jsonify

from ..common.responses import not_implemented_response
from ..middleware.authorization import login_required_json

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("", methods=["GET"])
@login_required_json
def list_tasks():
    """
    TODO (S1-04 — Aadi): List authenticated user's tasks with optional filters.
    TC-Task-01 | Requirement: TMA-F-010 | Backlog: S1-04
    """
    return jsonify(not_implemented_response("Task listing")), 501


@tasks_bp.route("", methods=["POST"])
@login_required_json
def create_task():
    """
    TODO (S1-04 — Aadi): Create a new task owned by the current user.
    TC-Task-01 | Requirement: TMA-F-010 | Backlog: S1-04
    """
    return jsonify(not_implemented_response("Task creation")), 501


@tasks_bp.route("/<int:task_id>", methods=["GET"])
@login_required_json
def get_task(task_id: int):
    """
    TODO (S1-04 — Aadi): Return a single task (owner-only).
    Requirement: TMA-F-010 | Backlog: S1-04
    """
    return jsonify(not_implemented_response("Task retrieval")), 501


@tasks_bp.route("/<int:task_id>", methods=["PATCH"])
@login_required_json
def update_task(task_id: int):
    """
    TODO (S1-04 — Aadi): Update an existing task.
    TC-Task-02 | Requirement: TMA-F-011 | Backlog: S1-04
    """
    return jsonify(not_implemented_response("Task update")), 501


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@login_required_json
def delete_task(task_id: int):
    """
    TODO (S1-05 — Aadi): Delete a task (owner or admin).
    TC-Task-03 | Requirement: TMA-F-012 | Backlog: S1-04
    """
    return jsonify(not_implemented_response("Task deletion")), 501

