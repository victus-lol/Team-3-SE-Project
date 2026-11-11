"""
Notification model.
Owner: Akash Pawar (PES2UG24CS041)
Sprint: S2 (S2-07)
Requirement IDs: TMA-F-040, TMA-F-041, TMA-F-042

Responsibilities:
  - Store per-user notification records linked optionally to a task
  - Status lifecycle: pending → delivered → read (or failed)
  - UTC timestamps throughout; no local-time mixing
  - Provider interface preserved; fake provider supported for tests
  - No default schedule invented (open decision — see DECISIONS_AND_OPEN_QUESTIONS.md)
"""

from datetime import datetime, timezone

from ..extensions import db


class Notification(db.Model):
    """A notification record for a user, optionally tied to a task."""

    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # task_id is nullable: some notifications may not relate to a specific task
    task_id = db.Column(
        db.Integer,
        db.ForeignKey("tasks.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    message = db.Column(db.String(512), nullable=False)
    scheduled_at = db.Column(db.DateTime(timezone=True), nullable=True)
    delivered_at = db.Column(db.DateTime(timezone=True), nullable=True)
    status = db.Column(
        db.String(20),
        nullable=False,
        default="pending",
        server_default="pending",
    )
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # ── CHECK constraints ─────────────────────────────────────────────────────
    __table_args__ = (
        db.CheckConstraint(
            "status IN ('pending', 'delivered', 'read', 'failed')",
            name="ck_notifications_status",
        ),
        db.CheckConstraint(
            "length(message) > 0",
            name="ck_notifications_message_nonempty",
        ),
    )

    # ── Relationships ─────────────────────────────────────────────────────────
    user = db.relationship("User", back_populates="notifications")
    task = db.relationship("Task", backref=db.backref("notifications", lazy="dynamic"))

    # ── Serialization ─────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "task_id": self.task_id,
            "message": self.message,
            "scheduled_at": self.scheduled_at.isoformat() if self.scheduled_at else None,
            "delivered_at": self.delivered_at.isoformat() if self.delivered_at else None,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        return f"<Notification id={self.id} user_id={self.user_id} status={self.status!r}>"
