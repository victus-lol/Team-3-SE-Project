
"""
Authentication routes.
Owner: Balaji Gowda S R (PES2UG25CS804)
Sprint: S1 (S1-03)
"""

from flask import Blueprint, jsonify, request
from flask_login import current_user
from flask_wtf.csrf import generate_csrf

from ..common.responses import (
    not_implemented_response,
    success_response,
)
from ..middleware.authorization import login_required_json
from .controller import handle_login, handle_logout

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/csrf", methods=["GET"])
def get_csrf_token():
    """Return a CSRF token for frontend requests."""
    token = generate_csrf()

    return jsonify(
        success_response(
            {"csrf_token": token},
            "CSRF token generated.",
        )
    ), 200


@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate a user and create a session."""
    request_data = request.get_json(silent=True)
    user_data = handle_login(request_data)

    return jsonify(
        success_response(user_data, "Login successful.")
    ), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """Terminate the current user session."""
    result = handle_logout()

    return jsonify(
        success_response(result, "Logout successful.")
    ), 200


@auth_bp.route("/me", methods=["GET"])
@login_required_json
def me():
    """Return the currently authenticated user's details."""
    return jsonify(
        success_response(
            current_user.to_dict(),
            "User details retrieved.",
        )
    ), 200


@auth_bp.route("/register", methods=["POST"])
def register():
    """Registration is outside the currently approved scope."""
    return jsonify(
        not_implemented_response("Registration (scope-pending)")
    ), 501
