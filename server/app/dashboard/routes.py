"""
Dashboard routes.
Owner: Balaji Gowda S R (PES2UG25CS804)
Sprint: S2 (S2-04)
Requirement IDs: TMA-F-033

Endpoints:
  GET /api/dashboard/summary → counts of pending/in_progress/completed tasks

TODO checklist:
  [x] Implement summary counts over current user's accessible tasks
  [x] Return counts in standard success envelope
  [x] Write integration tests in tests/integration/test_summary_api.py
"""

from flask import Blueprint, jsonify
from flask_login import current_user

from ..common.responses import success_response
from ..middleware.authorization import login_required_json
from .service import get_summary

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/summary", methods=["GET"])
@login_required_json
def summary():
    """
    Return task counts for the current user's dashboard.
    TC-Summary-01 | Requirement: TMA-F-033 | Backlog: S2-04
    """
    counts = get_summary(current_user.id)
    return jsonify(success_response(counts, "Dashboard summary retrieved successfully.")), 200

