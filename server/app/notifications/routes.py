"""
Notification routes.
Owner: Akash Pawar (PES2UG24CS041)
Sprint: S2 (S2-07)
Requirement IDs: TMA-F-040, TMA-F-041, TMA-F-042

Endpoints:
  GET   /api/notifications                         → list current user's notifications
  PATCH /api/notifications/<notification_id>/read  → mark owned notification as read
"""

from flask import Blueprint, jsonify
from flask_login import current_user

from ..common.responses import success_response
from ..middleware.authorization import login_required_json
from .service import list_notifications, mark_notification_read

notifications_bp = Blueprint("notifications", __name__)


@notifications_bp.route("", methods=["GET"])
@login_required_json
def list_notifications_route():
    """List only the authenticated user's notifications."""
    notifications = list_notifications(current_user.id)
    return jsonify(
        success_response(
            [notification.to_dict() for notification in notifications],
            "Notifications retrieved",
        )
    ), 200


@notifications_bp.route("/<int:notification_id>/read", methods=["PATCH"])
@login_required_json
def mark_read(notification_id: int):
    """Mark an owned notification as read; foreign IDs return 404."""
    notification = mark_notification_read(notification_id, current_user.id)
    return jsonify(
        success_response(notification.to_dict(), "Notification marked as read")
    ), 200
