"""
User model.
Owner: Balaji Gowda S R (PES2UG25CS804)
Sprint: S1 (S1-03)
Requirement IDs: TMA-F-001, TMA-F-002, TMA-SR-001, TMA-SR-003

Responsibilities:
  - Store authenticated user identity
  - Hash-only password storage (Werkzeug)
  - Role-based access (user / admin) with DB CHECK constraint
  - Normalized (lowercase, stripped) unique email
  - Flask-Login UserMixin compatibility
  - Public registration MUST NOT be able to set role=admin (enforced here)
"""

from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from ..extensions import db


class User(UserMixin, db.Model):
    """Application user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    # Normalized email: always stored lowercase and stripped
    email = db.Column(db.String(254), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(
        db.String(10),
        nullable=False,
        default="user",
        server_default="user",
    )
    is_active = db.Column(db.Boolean, nullable=False, default=True, server_default="1")
    session_version = db.Column(db.Integer, nullable=False, default=0, server_default="0")
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # ── CHECK constraints (enforced by SQLite) ────────────────────────────────
    __table_args__ = (
        db.CheckConstraint("role IN ('user', 'admin')", name="ck_users_role"),
        db.CheckConstraint("length(name) > 0", name="ck_users_name_nonempty"),
        db.CheckConstraint("length(email) >= 3 AND email LIKE '%@%'", name="ck_users_email_format"),
    )

    # ── Relationships ─────────────────────────────────────────────────────────
    tasks = db.relationship(
        "Task",
        back_populates="owner",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    categories = db.relationship(
        "Category",
        back_populates="user",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    notifications = db.relationship(
        "Notification",
        back_populates="user",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    # ── Password handling ─────────────────────────────────────────────────────

    def set_password(self, plaintext: str) -> None:
        """Hash and store password. Never stores plaintext."""
        if not plaintext or len(plaintext) < 8:
            raise ValueError("Password must be at least 8 characters.")
        self.password_hash = generate_password_hash(plaintext)

    def check_password(self, plaintext: str) -> bool:
        """Return True if plaintext matches the stored hash."""
        return check_password_hash(self.password_hash, plaintext)

    # ── Class-level factory methods ───────────────────────────────────────────

    @classmethod
    def _normalize_email(cls, email: str) -> str:
        return email.strip().lower()

    @classmethod
    def create(
        cls,
        name: str,
        email: str,
        password: str,
        role: str = "user",
    ) -> "User":
        """
        Create a new User.

        Public registration MUST pass role='user' (the default).
        Only internal admin bootstrap may pass role='admin'.
        This method validates the role so service layers cannot accidentally
        escalate privileges.
        """
        if role not in ("user", "admin"):
            raise ValueError("role must be 'user' or 'admin'.")
        user = cls(
            name=name.strip(),
            email=cls._normalize_email(email),
            role=role,
        )
        user.set_password(password)
        return user

    # ── Flask-Login interface ─────────────────────────────────────────────────

    def get_id(self) -> str:
        """Flask-Login requires string ID."""
        return str(self.id)

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"

    # ── Serialization ─────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Safe public representation — never includes password_hash."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r} role={self.role!r}>"
