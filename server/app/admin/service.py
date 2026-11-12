"""Admin user-management queries and minimal audit persistence."""

import logging

from sqlalchemy.exc import SQLAlchemyError

from ..extensions import db
from ..models.audit_log import AuditLog
from ..models.user import User

logger = logging.getLogger(__name__)


def list_users(page: int = 1, per_page: int = 20) -> list:
    """Return a stable page of users without exposing authentication secrets."""
    return User.query.order_by(User.id.asc()).paginate(
        page=max(1, page), per_page=min(max(1, per_page), 100), error_out=False
    ).items


def record_audit_event(actor_id: int, action: str, target_type: str | None = None, target_id: str | None = None) -> None:
    """Persist a secret-free audit event without blocking the business request."""
    try:
        db.session.add(
            AuditLog(actor_id=actor_id, action=action, target_type=target_type, target_id=target_id)
        )
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        logger.exception("Could not persist administrator audit event: %s", action)


def list_audit_logs(page: int = 1, per_page: int = 50):
    """Return the newest audit events for an administrator review page."""
    return AuditLog.query.order_by(AuditLog.created_at.desc(), AuditLog.id.desc()).paginate(
        page=max(1, page), per_page=min(max(1, per_page), 100), error_out=False
    )
