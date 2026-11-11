"""
Common response helpers — standardized JSON formats used across all routes.
Owner: Akash Pawar (PES2UG24CS041)
"""


def success_response(
    data: dict | list | None = None, message: str = "Operation successful"
) -> dict:
    """Build a standard success envelope."""
    return {
        "success": True,
        "data": data if data is not None else {},
        "message": message,
    }


def error_response(code: str, message: str, details: dict | None = None) -> dict:
    """Build a standard error envelope. Never include internal details in production."""
    payload: dict = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
        },
    }
    if details:
        payload["error"]["details"] = details
    return payload


def not_implemented_response(feature: str = "This feature") -> dict:
    """Used by skeleton routes not yet implemented."""
    return error_response(
        "NOT_IMPLEMENTED",
        f"{feature} has not been implemented yet.",
    )
