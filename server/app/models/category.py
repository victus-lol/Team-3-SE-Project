"""
Category model.
Owner: Aadi Kore (PES2UG24CS006)
Sprint: S1 (S1-04), S2 (S2-01)
Requirement IDs: TMA-F-030, TMA-F-031

Responsibilities:
  - Categories belong to a single user (not global)
  - Name unique per user (case-insensitive: stored lowercase; see NOTE below)
  - A category MUST NOT be assigned to another user's task
    → Enforced in service layer (TaskService validates category ownership)
    → SQLite cannot express cross-table ownership CHECK natively; documented here.

NOTE on case-insensitive uniqueness:
  The UniqueConstraint on (user_id, name) is case-sensitive in SQLite by default.
  We normalize name to lowercase on write (via the Category.create() factory)
  to achieve case-insensitive uniqueness at the application layer.
  ASSUMPTION: case-insensitive matching is sufficient for MVP.
"""

from datetime import datetime, timezone

from ..extensions import db


class Category(db.Model):
    """A user-owned label that can be applied to tasks."""

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # Stored lowercase for case-insensitive uniqueness
    name = db.Column(db.String(100), nullable=False)
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

    # ── Constraints ───────────────────────────────────────────────────────────
    __table_args__ = (
        db.UniqueConstraint("user_id", "name", name="uq_categories_user_name"),
        db.CheckConstraint("length(name) > 0", name="ck_categories_name_nonempty"),
        db.CheckConstraint("length(name) <= 100", name="ck_categories_name_maxlen"),
    )

    # ── Relationships ─────────────────────────────────────────────────────────
    user = db.relationship("User", back_populates="categories")
    tasks = db.relationship(
        "Task",
        back_populates="category",
        lazy="dynamic",
        # Do NOT cascade-delete tasks when a category is removed;
        # the FK is SET NULL so tasks become uncategorized.
    )

    # ── Factory ───────────────────────────────────────────────────────────────

    @classmethod
    def create(cls, user_id: int, name: str) -> "Category":
        """Create a category with normalized (lowercase, stripped) name."""
        normalized = name.strip().lower()
        if not normalized:
            raise ValueError("Category name cannot be empty.")
        return cls(user_id=user_id, name=normalized)

    # ── Serialization ─────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        return f"<Category id={self.id} name={self.name!r} user_id={self.user_id}>"

