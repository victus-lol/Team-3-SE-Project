"""
Authentication routes.
Owner: Balaji Gowda S R (PES2UG25CS804)
Sprint: S1 (S1-03)
Requirement IDs: TMA-F-001, TMA-F-002, TMA-SR-001, TMA-SR-003

Implemented endpoints:
  GET  /api/auth/csrf      → returns CSRF token (security foundation, live)
  POST /api/auth/login     → authenticate user (skeleton, S1-03)
  POST /api/auth/logout    → end session (skeleton, S1-03)
  GET  /api/auth/me        → current user info (skeleton, S1-03)
  POST /api/auth/register  → create account (scope-pending, returns 501)

TODO checklist (S1-03):
  [ ] Implement login with email + password validation
  [ ] Implement logout clearing session
  [ ] Implement /me returning current_user.to_dict()
  [ ] Validate login input; return 401 on invalid credentials
  [ ] Hash password on registration when scope is approved
  [ ] Write integration tests in tests/integration/test_auth_api.py
"""

from flask import Blueprint, jsonify
from flask_wtf.csrf import generate_csrf

from ..common.responses import not_implemented_response, success_response

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/csrf", methods=["GET"])
def get_csrf_token():
    """
    Return a CSRF token for the frontend to include in X-CSRFToken header.
    This endpoint is LIVE as part of the security foundation.
    """
    token = generate_csrf()
    return jsonify(success_response({"csrf_token": token}, "CSRF token generated")), 200


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    TODO (S1-03 — Balaji): Implement user login.
    TC-Auth-01, TC-Auth-02 | Requirement: TMA-F-001 | Backlog: S1-03
    """
    return jsonify(not_implemented_response("Login")), 501


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """
    TODO (S1-03 — Balaji): Implement logout, clear session.
    TC-Auth-03 | Requirement: TMA-F-002 | Backlog: S1-03
    """
    return jsonify(not_implemented_response("Logout")), 501


@auth_bp.route("/me", methods=["GET"])
def me():
    """
    TODO (S1-03 — Balaji): Return current authenticated user.
    Requirement: TMA-F-001 | Backlog: S1-03
    """
    return jsonify(not_implemented_response("Current user")), 501


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Scope-pending: registration acceptance criteria not yet approved.
    See DECISIONS_AND_OPEN_QUESTIONS.md item (1).
    """
    return jsonify(not_implemented_response("Registration (scope-pending)")), 501

