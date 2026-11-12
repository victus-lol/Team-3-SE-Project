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

from flask import Blueprint, jsonify

from ..common.responses import success_response
from ..middleware.authorization import admin_required
from .service import list_users as get_users

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/users", methods=["GET"])
@admin_required
def list_users():
    """List users safely for authenticated administrators."""
    users = get_users()
    return jsonify(success_response([user.to_dict() for user in users])), 200
