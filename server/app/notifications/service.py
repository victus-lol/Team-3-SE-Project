"""
Notification service — reminder generation and delivery coordination.
Owner: Akash Pawar (PES2UG24CS041)
Sprint: S2 (S2-07)
Requirement IDs: TMA-F-040, TMA-F-041, TMA-F-042

All persisted timestamps use UTC. No default reminder time is invented:
a notification without scheduled_at is eligible for immediate dispatch.
"""

import logging
from datetime import datetime, timezone

from ..common.exceptions import NotFoundError, ValidationError
from ..extensions import db
from ..models.notification import Notification
from ..models.task import Task
from ..models.user import User

logger = logging.getLogger(__name__)


def _normalize_utc(value: datetime | None) -> datetime | None:
    """Validate a supplied datetime and normalize it to aware UTC."""
    if value is None:
        return None
    if not isinstance(value, datetime):
        raise ValidationError("scheduled_at must be a datetime value.")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValidationError("scheduled_at must include a timezone.")
    return value.astimezone(timezone.utc)


def list_notifications(user_id: int) -> list[Notification]:
    """Return notifications belonging only to user_id, newest first."""
    return (
        Notification.query.filter_by(user_id=user_id)
        .order_by(Notification.created_at.desc(), Notification.id.desc())
        .all()
    )


def create_notification(
    user_id: int,
    message: str,
    task_id: int | None = None,
    scheduled_at: datetime | None = None,
) -> Notification:
    """
    Persist a notification for a user.

    A linked task must belong to that same user. This prevents a caller from
    creating a notification that exposes another user's task identifier.
    """
    if not isinstance(message, str) or not message.strip():
        raise ValidationError("Notification message cannot be empty.")
    normalized_message = message.strip()
    if len(normalized_message) > 512:
        raise ValidationError("Notification message cannot exceed 512 characters.")

    user = db.session.get(User, user_id)
    if user is None:
        raise NotFoundError("User not found.")

    if task_id is not None:
        task = Task.query.filter_by(id=task_id, owner_id=user_id).first()
        if task is None:
            raise NotFoundError("Task not found.")

    notification = Notification(
        user_id=user.id,
        task_id=task_id,
        message=normalized_message,
        scheduled_at=_normalize_utc(scheduled_at),
        status="pending",
    )
    db.session.add(notification)
    db.session.commit()
    return notification


def mark_notification_read(notification_id: int, user_id: int) -> Notification:
    """
    Mark a notification as read, enforcing ownership at query time.

    Return 404 for both a missing notification and another user's notification
    so the API does not reveal whether another user's record exists.
    """
    notification = Notification.query.filter_by(
        id=notification_id,
        user_id=user_id,
    ).first()
    if notification is None:
        raise NotFoundError("Notification not found.")

    if notification.status != "read":
        notification.status = "read"
        db.session.commit()
    return notification


def dispatch_notification(
    notification_id: int,
    provider,
    *,
    now: datetime | None = None,
) -> Notification:
    """
    Attempt one delivery through the injected provider.

    Future reminders remain pending. Provider failures transition the record
    to 'failed'; successful sends transition it to 'delivered' and set the
    UTC delivered_at timestamp. Already processed records are not sent again.
    """
    notification = db.session.get(Notification, notification_id)
    if notification is None:
        raise NotFoundError("Notification not found.")

    if notification.status != "pending":
        return notification

    current_time = _normalize_utc(now) if now is not None else datetime.now(timezone.utc)
    scheduled_at = notification.scheduled_at
    if scheduled_at is not None and scheduled_at.tzinfo is None:
        # SQLite stores timezone-aware DateTime values without the tzinfo;
        # project policy states that these stored timestamps are UTC.
        scheduled_at = scheduled_at.replace(tzinfo=timezone.utc)
    elif scheduled_at is not None:
        scheduled_at = scheduled_at.astimezone(timezone.utc)

    if scheduled_at is not None and scheduled_at > current_time:
        return notification

    try:
        sent = provider.send(
            user_id=notification.user_id,
            message=notification.message,
            task_id=notification.task_id,
        )
    except Exception:
        logger.exception("Notification provider raised while sending id=%s", notification.id)
        sent = False

    if sent:
        notification.status = "delivered"
        notification.delivered_at = current_time
    else:
        notification.status = "failed"

    db.session.commit()
    return notification
