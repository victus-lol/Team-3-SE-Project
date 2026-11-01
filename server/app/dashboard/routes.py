"""
Dashboard routes.
Owner: Balaji Gowda S R (PES2UG25CS804)
Sprint: S2 (S2-04)
Requirement IDs: TMA-F-033

Endpoints:
  GET /api/dashboard/summary → counts of pending/in_progress/completed tasks

TODO checklist:
  [ ] Implement summary counts over current user's accessible tasks
  [ ] Return counts in standard success envelope
  [ ] Write integration tests in tests/integration/test_summary_api.py
"""

from flask import Blueprint, jsonify

from ..common.responses import not_implemented_response
from ..middleware.authorization import login_required_json

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/summary", methods=["GET"])
@login_required_json
def summary():
    """
    TODO (S2-04 — Balaji): Return task counts for the current user's dashboard.
    TC-Summary-01 | Requirement: TMA-F-033 | Backlog: S2-04
    """
    return jsonify(not_implemented_response("Dashboard summary")), 501

