"""Authentication service — business logic layer.
Owner: Balaji Gowda S R (PES2UG25CS804)
Sprint: S1 (S1-03)
"""

import re

from sqlalchemy.exc import IntegrityError

from ..common.exceptions import (
    AuthenticationError,
    ConflictError,
    ValidationError,
)
from ..extensions import db
from ..models.user import User


def authenticate(email: str, password: str) -> User:
    """Authenticate a user using email and password."""

    if not isinstance(email, str) or not email.strip():
        raise AuthenticationError("Invalid email or password.")

    if not isinstance(password, str) or not password:
        raise AuthenticationError("Invalid email or password.")

    user = get_user_by_email(email)

    if user is None or not user.check_password(password):
        raise AuthenticationError("Invalid email or password.")

    if not user.is_active:
        raise AuthenticationError("Invalid email or password.")

    return user


def create_admin_user(name: str, email: str, password: str) -> User:
    """Create an administrator account through the CLI."""

    normalized_email = email.strip().lower()
    existing = get_user_by_email(normalized_email)

    if existing:
        raise ConflictError(f"A user with email '{normalized_email}' already exists.")

    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters.")

    admin = User.create(
        name=name,
        email=normalized_email,
        password=password,
        role="admin",
    )

    db.session.add(admin)
    db.session.commit()

    return admin


def create_registered_user(name: str, email: str, password: str) -> User:
    """Create a standard user without allowing public role assignment."""
    if not isinstance(name, str) or not name.strip() or len(name.strip()) > 128:
        raise ValidationError("Name must contain 1 to 128 characters.")
    if not isinstance(email, str) or len(email.strip()) > 254:
        raise ValidationError("Enter a valid email address.")
    if not isinstance(password, str) or len(password) < 8 or len(password) > 128:
        raise ValidationError("Password must contain 8 to 128 characters.")

    normalized_email = email.strip().lower()
    if not re.fullmatch(r"[^@\s]+@[^@\s.]+(?:\.[^@\s.]+)+", normalized_email):
        raise ValidationError("Enter a valid email address.")
    if get_user_by_email(normalized_email):
        raise ConflictError("An account with this email already exists.")

    user = User.create(name.strip(), normalized_email, password, role="user")
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise ConflictError("An account with this email already exists.") from exc
    return user


def get_user_by_email(email: str) -> User | None:
    """Look up a user using a normalized email address."""

    return User.query.filter_by(email=email.strip().lower()).first()
