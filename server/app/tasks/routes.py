"""
Task routes.
Owner: Aadi Kore (PES2UG24CS006)
"""

from flask import Blueprint, jsonify, request
from flask_login import current_user

from ..common.exceptions import ValidationError
from ..common.responses import success_response
from ..middleware.authorization import login_required_json
from ..search.service import search_tasks_query
from .controller import handle_create_task, handle_update_task
from .service import (
    delete_task,
    get_task_or_404,
)

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("", methods=["GET"])
@login_required_json
def list_tasks_route():
    params = request.args.to_dict()
    page = _positive_integer(params.pop("page", "1"), "page")
    per_page = _positive_integer(params.pop("per_page", "20"), "per_page")
    if per_page > 100:
        raise ValidationError("per_page must not exceed 100.")

    pagination = search_tasks_query(current_user.id, params).paginate(
        page=page, per_page=per_page, error_out=False
    )
    response = success_response([task.to_dict() for task in pagination.items])
    response["pagination"] = {
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total_items": pagination.total,
        "total_pages": pagination.pages,
        "has_next": pagination.has_next,
        "has_previous": pagination.has_prev,
    }
    return jsonify(response), 200


def _positive_integer(value: str, field: str) -> int:
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{field} must be a positive integer.") from exc
    if result < 1:
        raise ValidationError(f"{field} must be a positive integer.")
    return result


@tasks_bp.route("", methods=["POST"])
@login_required_json
def create_task_route():
    data = request.get_json(silent=True)

    result = handle_create_task(current_user.id, data)

    return jsonify(success_response(result, "Task created successfully.")), 201


@tasks_bp.route("/<int:task_id>", methods=["GET"])
@login_required_json
def get_task_route(task_id: int):
    task = get_task_or_404(task_id, current_user.id)

    return jsonify(success_response(task.to_dict())), 200


@tasks_bp.route("/<int:task_id>", methods=["PATCH"])
@login_required_json
def update_task_route(task_id: int):
    data = request.get_json(silent=True)

    result = handle_update_task(
        task_id,
        current_user.id,
        data,
    )

    return jsonify(success_response(result, "Task updated successfully.")), 200


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@login_required_json
def delete_task_route(task_id: int):
    delete_task(task_id, current_user.id)

    return jsonify(success_response({}, "Task deleted successfully.")), 200
