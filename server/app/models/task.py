"""
Task model.
Owner: Aadi Kore (PES2UG24CS006)
Sprint: S1 (S1-04, S1-05), S2 (S2-01, S2-02)
Requirement IDs: TMA-F-010, TMA-F-011, TMA-F-012, TMA-F-020, TMA-F-021

Responsibilities:
  - Core task entity with priority, due date, status, category
  - CHECK constraints on priority and status (DB-enforced)
  - Ownership FK to User; tasks NEVER accessible by other users
  - Optional category FK (nullable); cascade policy defined below
  - Sensible field lengths and non-empty title
  - Indexes for owner lookups and filtering
"""

from datetime import datetime, timezone

from ..extensions import db


class Task(db.Model):
    """A task belonging to a single user."""

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(10), nullable=False, default="medium", server_default="medium")
    # Stored as TEXT date 'YYYY-MM-DD' to avoid timezone confusion
    due_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="pending", server_default="pending")
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
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

    # ── CHECK constraints ─────────────────────────────────────────────────────
    __table_args__ = (
        db.CheckConstraint(
            "priority IN ('low', 'medium', 'high')",
            name="ck_tasks_priority",
        ),
        db.CheckConstraint(
            "status IN ('pending', 'in_progress', 'completed')",
            name="ck_tasks_status",
        ),
        db.CheckConstraint(
            "length(title) > 0",
            name="ck_tasks_title_nonempty",
        ),
        db.CheckConstraint(
            "length(title) <= 200",
            name="ck_tasks_title_maxlen",
        ),
        # Composite index for owner + status queries
        db.Index("ix_tasks_owner_status", "owner_id", "status"),
        db.Index("ix_tasks_owner_priority", "owner_id", "priority"),
        db.Index("ix_tasks_owner_due_date", "owner_id", "due_date"),
    )

    # ── Relationships ─────────────────────────────────────────────────────────
    owner = db.relationship("User", back_populates="tasks")
    category = db.relationship("Category", back_populates="tasks")

    # ── Serialization ─────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "status": self.status,
            "category_id": self.category_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        return f"<Task id={self.id} title={self.title!r} status={self.status!r}>"

