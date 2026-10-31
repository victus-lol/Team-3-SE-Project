"""
Custom exception classes for the Task Manager API.
Owner: Akash Pawar (PES2UG24CS041), coordinated with Balaji Gowda S R (PES2UG25CS804)
"""


class AppError(Exception):
    """Base application error. Always maps to a structured JSON response."""

    status_code: int = 500
    code: str = "INTERNAL_ERROR"

    def __init__(self, message: str = "An unexpected error occurred.", details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.details = details


class ValidationError(AppError):
    status_code = 400
    code = "VALIDATION_ERROR"

    def __init__(self, message: str = "Invalid input.", details: dict | None = None):
        super().__init__(message, details)


class AuthenticationError(AppError):
    status_code = 401
    code = "AUTHENTICATION_ERROR"

    def __init__(self, message: str = "Authentication required."):
        super().__init__(message)


class AuthorizationError(AppError):
    status_code = 403
    code = "AUTHORIZATION_ERROR"

    def __init__(self, message: str = "You do not have permission to perform this action."):
        super().__init__(message)


class NotFoundError(AppError):
    status_code = 404
    code = "NOT_FOUND"

    def __init__(self, message: str = "Resource not found."):
        super().__init__(message)


class ConflictError(AppError):
    status_code = 409
    code = "CONFLICT"

    def __init__(self, message: str = "Resource already exists."):
        super().__init__(message)

