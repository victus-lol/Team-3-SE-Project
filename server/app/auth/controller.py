"""
Authentication controller — request/response handling.
Owner: Balaji Gowda S R (PES2UG25CS804)
Sprint: S1 (S1-03)
"""

from flask_login import login_user, logout_user

from ..common.exceptions import (
    AuthenticationError,
    ValidationError,
)
from .service import authenticate


def handle_login(request_data: dict) -> dict:
    """
    Validate login data, authenticate the user,
    and create a Flask-Login session.
    """

    if not isinstance(request_data, dict):
        raise ValidationError("A valid JSON request body is required.")

    email = request_data.get("email")
    password = request_data.get("password")

    if (
        not isinstance(email, str)
        or not email.strip()
        or not isinstance(password, str)
        or not password
    ):
        raise ValidationError("Email and password are required.")

    user = authenticate(email, password)

    if not login_user(user):
        raise AuthenticationError("Invalid email or password.")

    # User.to_dict() excludes password_hash.
    return user.to_dict()


def handle_logout() -> dict:
    """
    Terminate the current Flask-Login session.
    """
    logout_user()
    return {"logged_out": True}
