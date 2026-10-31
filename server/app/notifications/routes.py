"""
Notification routes.
Owner: Akash Pawar (PES2UG24CS041)
Sprint: S2 (S2-07)
Requirement IDs: TMA-F-040, TMA-F-041, TMA-F-042

Endpoints:
  GET   /api/notifications                         → list user's notifications
  PATCH /api/notifications/<notification_id>/read  → mark as read

TODO checklist:
  [ ] Implement list notifications (user-scoped)
  [ ] Implement mark-as-read endpoint
  [ ] Integrate with provider and scheduler skeletons
  [ ] Write integration tests in tests/integration/test_notifications_api.py
"""

from flask import Blueprint, jsonify

from ..common.responses import not_implemented_response
from ..middleware.authorization import login_required_json

notifications_bp = Blueprint("notifications", __name__)


@notifications_bp.route("", methods=["GET"])
@login_required_json
def list_notifications():
    """
    TODO (S2-07 — Akash): List current user's notifications.
    TC-Notify-01 | Requirement: TMA-F-040 | Backlog: S2-07
    """
    return jsonify(not_implemented_response("Notification listing")), 501


@notifications_bp.route("/<int:notification_id>/read", methods=["PATCH"])
@login_required_json
def mark_read(notification_id: int):
    """
    TODO (S2-07 — Akash): Mark a notification as read.
    Requirement: TMA-F-041 | Backlog: S2-07
    """
    return jsonify(not_implemented_response("Mark notification read")), 501

