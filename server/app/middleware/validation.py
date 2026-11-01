"""
Request validation middleware.
Owner: Balaji Gowda S R (PES2UG25CS804), coordinated with Aadi Kore (PES2UG24CS006)
"""

from flask import jsonify, request

from ..common.responses import error_response


def require_json(f):
    """Decorator: require Content-Type: application/json on the request."""
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.is_json:
            return (
                jsonify(
                    error_response(
                        "VALIDATION_ERROR",
                        "Request Content-Type must be application/json.",
                    )
                ),
                400,
            )
        return f(*args, **kwargs)
    return decorated

