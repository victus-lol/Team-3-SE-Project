"""
Authentication service — business logic layer.
Owner: Balaji Gowda S R (PES2UG25CS804)
Sprint: S1 (S1-03), S2 (S2-06)
Requirement IDs: TMA-F-001, TMA-F-002, TMA-SR-001, TMA-SR-003

Responsibilities:
  - User authentication (email + password)
  - Session management via Flask-Login
  - Password hashing (Werkzeug only; no plaintext storage)
  - Admin user bootstrap via CLI

TODO checklist:
  [ ] Implement authenticate(email, password) → User
  [ ] Raise AuthenticationError on invalid credentials (never reveal which field)
  [ ] Implement login_user / logout_user wrappers
  [ ] Implement get_current_user()
  [ ] Write unit tests in tests/unit/test_auth_service.py
"""

from ..common.exceptions import ConflictError, ValidationError
from ..extensions import db
from ..models.user import User


def authenticate(email: str, password: str) -> User:
    """
    TODO (S1-03 — Balaji): Authenticate a user by email and password.
    - Normalize email before lookup
    - Return the User on success
    - Raise AuthenticationError on failure (do not reveal which field is wrong)
    """
    raise NotImplementedError("authenticate() not yet implemented (S1-03)")


def create_admin_user(name: str, email: str, password: str) -> User:
    """
    Create an administrator account. Called only by the CLI command.
    This is part of the security foundation (Part A).
    """
    normalized_email = email.strip().lower()
    existing = User.query.filter_by(email=normalized_email).first()
    if existing:
        raise ConflictError(f"A user with email '{normalized_email}' already exists.")

    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters.")

    admin = User.create(name=name, email=normalized_email, password=password, role="admin")
    db.session.add(admin)
    db.session.commit()
    return admin


def get_user_by_email(email: str) -> User | None:
    """Look up a user by normalized email. Returns None if not found."""
    return User.query.filter_by(email=email.strip().lower()).first()

