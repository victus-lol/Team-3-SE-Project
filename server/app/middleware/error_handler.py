"""
Centralized error handler registration.
Owner: Balaji Gowda S R (PES2UG25CS804), coordinated with Akash Pawar (PES2UG24CS041)
"""

from flask import Flask, jsonify

from ..common.exceptions import AppError
from ..common.responses import error_response


def register_error_handlers(app: Flask) -> None:
    """Attach JSON error handlers to the Flask app instance."""

    @app.errorhandler(AppError)
    def handle_app_error(exc: AppError):
        response = error_response(exc.code, exc.message, exc.details)
        return jsonify(response), exc.status_code

    @app.errorhandler(400)
    def bad_request(exc):
        return jsonify(error_response("BAD_REQUEST", "Bad request.")), 400

    @app.errorhandler(401)
    def unauthorized(exc):
        return jsonify(error_response("AUTHENTICATION_ERROR", "Authentication required.")), 401

    @app.errorhandler(403)
    def forbidden(exc):
        return jsonify(error_response("AUTHORIZATION_ERROR", "Forbidden.")), 403

    @app.errorhandler(404)
    def not_found(exc):
        return jsonify(error_response("NOT_FOUND", "Resource not found.")), 404

    @app.errorhandler(405)
    def method_not_allowed(exc):
        return jsonify(error_response("METHOD_NOT_ALLOWED", "Method not allowed.")), 405

    @app.errorhandler(422)
    def unprocessable(exc):
        return jsonify(error_response("VALIDATION_ERROR", "Unprocessable entity.")), 422

    @app.errorhandler(429)
    def too_many_requests(exc):
        return jsonify(error_response("RATE_LIMITED", "Too many requests.")), 429

    @app.errorhandler(500)
    def internal_error(exc):
        # Never expose details in production
        app.logger.exception("Unhandled server error")
        return jsonify(error_response("INTERNAL_ERROR", "An unexpected error occurred.")), 500

