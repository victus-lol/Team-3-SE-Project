"""
Authorization middleware — reusable decorators.
Owner: Balaji Gowda S R (PES2UG25CS804), coordinated with Aadi Kore (PES2UG24CS006)
Sprint: S1 (S1-03), S2 (S2-06)
Requirement IDs: TMA-SR-001, TMA-SR-003
"""

from functools import wraps

from flask import jsonify
from flask_login import current_user

from ..common.responses import error_response


def login_required_json(f):
    """
    Like Flask-Login's @login_required but returns JSON 401 instead of
    redirecting to the login page. Use on all API routes.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return (
                jsonify(error_response("AUTHENTICATION_ERROR", "Authentication required.")),
                401,
            )
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    """
    Requires the current user to be authenticated AND have the 'admin' role.
    Returns 401 if not logged in, 403 if logged in but not admin.
    Never relies on frontend-only visibility.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return (
                jsonify(error_response("AUTHENTICATION_ERROR", "Authentication required.")),
                401,
            )
        if not current_user.is_admin:
            return (
                jsonify(error_response("AUTHORIZATION_ERROR", "Admin access required.")),
                403,
            )
        return f(*args, **kwargs)
    return decorated


def owner_required(model_cls, id_param: str = "task_id", user_field: str = "owner_id"):
    """
    Decorator factory: loads a model by `id_param`, verifies the current user
    owns it (or is admin), and injects the instance as `resource` kwarg.

    Returns 404 (not 403) when the resource does not exist or belongs to
    another user — prevents enumeration.

    Design choice: 404 is returned for unauthorized access to another user's
    resource. This is consistent and documented in DECISIONS_AND_OPEN_QUESTIONS.md.
    """
    def decorator(f):
        @wraps(f)
        @login_required_json
        def decorated(*args, **kwargs):
            resource_id = kwargs.get(id_param)
            resource = model_cls.query.get(resource_id)
            if resource is None:
                return jsonify(error_response("NOT_FOUND", "Resource not found.")), 404
            owner_id = getattr(resource, user_field, None)
            if owner_id != current_user.id and not current_user.is_admin:
                # Return 404 to avoid confirming resource existence
                return jsonify(error_response("NOT_FOUND", "Resource not found.")), 404
            kwargs["resource"] = resource
            return f(*args, **kwargs)
        return decorated
    return decorator

