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

from ..common.responses import not_implemented_response
from ..middleware.authorization import admin_required

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/users", methods=["GET"])
@admin_required
def list_users():
    """
    TODO (S2-06 — Balaji): List all users (admin only).
    TC-Admin-01 | Requirement: TMA-SR-001 | Backlog: S2-06
    """
    return jsonify(not_implemented_response("Admin user listing")), 501
