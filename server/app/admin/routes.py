"""
Admin routes.
Owner: Balaji Gowda S R (PES2UG25CS804)
Sprint: S2 (S2-06)
Requirement IDs: TMA-SR-001, TMA-SR-003

Endpoints:
  GET /api/admin/users → list all users (admin only)

TODO checklist:
  [ ] Implement user listing (paginated)
  [ ] Ensure standard users always receive 403
  [ ] Write integration tests in tests/integration/test_admin_api.py
"""

from flask import Blueprint, jsonify, request
from flask_login import current_user

from ..common.exceptions import ValidationError
from ..common.responses import success_response
from ..middleware.authorization import admin_required
from .service import list_audit_logs, record_audit_event
from .service import list_users as get_users

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/users", methods=["GET"])
@admin_required
def list_users():
    """List users safely for authenticated administrators."""
    users = get_users()
    record_audit_event(current_user.id, "admin.users.listed", "user_collection")
    return jsonify(success_response([user.to_dict() for user in users])), 200


@admin_bp.route("/audit-logs", methods=["GET"])
@admin_required
def get_audit_logs():
    """Return a paginated, secret-free administrator audit history."""
    page = _positive_integer(request.args.get("page", "1"), "page")
    per_page = _positive_integer(request.args.get("per_page", "50"), "per_page")
    if per_page > 100:
        raise ValidationError("per_page must not exceed 100.")

    pagination = list_audit_logs(page, per_page)
    record_audit_event(current_user.id, "admin.audit_logs.viewed", "audit_log_collection")
    response = success_response([entry.to_dict() for entry in pagination.items])
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
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{field} must be a positive integer.") from exc
    if number < 1:
        raise ValidationError(f"{field} must be a positive integer.")
    return number
