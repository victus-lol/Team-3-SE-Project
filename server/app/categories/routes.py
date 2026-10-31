"""
Category routes.
Owner: Aadi Kore (PES2UG24CS006)
Sprint: S2 (S2-01) — scope-pending for create (see DECISIONS_AND_OPEN_QUESTIONS.md item 2)
Requirement IDs: TMA-F-030, TMA-F-031

Endpoints:
  GET  /api/categories → list current user's categories
  POST /api/categories → create a category (scope-pending)

TODO checklist:
  [ ] Implement list_categories (user's own categories only)
  [ ] Implement create_category (validate ownership, unique name per user)
  [ ] Write integration tests in tests/integration/test_categories_api.py
"""

from flask import Blueprint, jsonify

from ..common.responses import not_implemented_response
from ..middleware.authorization import login_required_json

categories_bp = Blueprint("categories", __name__)


@categories_bp.route("", methods=["GET"])
@login_required_json
def list_categories():
    """
    TODO (S2-01 — Aadi): List authenticated user's categories.
    TC-Org-04 | Requirement: TMA-F-030 | Backlog: S2-01
    """
    return jsonify(not_implemented_response("Category listing")), 501


@categories_bp.route("", methods=["POST"])
@login_required_json
def create_category():
    """
    TODO (S2-01 — Aadi): Create category (scope-pending decision).
    Requirement: TMA-F-031 | Backlog: S2-01
    """
    return jsonify(not_implemented_response("Category creation (scope-pending)")), 501

