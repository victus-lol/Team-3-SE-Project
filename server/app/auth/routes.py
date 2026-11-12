"""
Authentication routes.
Owner: Balaji Gowda S R (PES2UG25CS804)
Sprint: S1 (S1-03)
"""

from flask import Blueprint, jsonify, request
from flask_login import current_user
from flask_wtf.csrf import generate_csrf

from ..common.exceptions import AuthenticationError, RateLimitError, ValidationError
from ..common.responses import (
    success_response,
)
from ..middleware.authorization import login_required_json
from .controller import handle_login, handle_logout
from .service import create_registered_user
from .throttle import clear_login_failures, is_login_locked, record_failed_login

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
    email = request_data.get("email") if isinstance(request_data, dict) else None
    client_address = request.remote_addr
    if is_login_locked(email, client_address):
        raise RateLimitError("Invalid email or password. Please try again later.")
    try:
        user_data = handle_login(request_data)
    except AuthenticationError:
        record_failed_login(email, client_address)
        raise
    clear_login_failures(email, client_address)

    return jsonify(success_response(user_data, "Login successful.")), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """Terminate the current user session."""
    result = handle_logout()

    return jsonify(success_response(result, "Logout successful.")), 200


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
    """Register a standard user; role assignment remains administrator-only."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValidationError("A valid JSON request body is required.")
    user = create_registered_user(data.get("name"), data.get("email"), data.get("password"))
    return jsonify(success_response(user.to_dict(), "Account created successfully.")), 201
