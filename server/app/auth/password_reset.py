"""Password reset token generation, delivery, and confirmation."""

import hashlib
import logging
import secrets
import time
from urllib.parse import urlencode

from flask import current_app

from ..common.exceptions import ValidationError
from ..extensions import db
from ..models.password_reset_token import PasswordResetToken
from ..models.user import User
from .mail import send_password_reset_email
from .service import get_user_by_email

logger = logging.getLogger(__name__)


def request_password_reset(email: str | None, now: float | None = None) -> None:
    """Queue a reset email without disclosing account existence to callers."""
    if not isinstance(email, str) or not email.strip():
        return
    user = get_user_by_email(email)
    if user is None or not user.is_active:
        return

    now = time.time() if now is None else now
    token = secrets.token_urlsafe(32)
    token_record = PasswordResetToken(
        user_id=user.id,
        token_hash=_hash_token(token),
        created_at=now,
        expires_at=now + current_app.config["PASSWORD_RESET_TOKEN_TTL_SECONDS"],
    )
    PasswordResetToken.query.filter_by(user_id=user.id, used_at=None).update({"used_at": now})
    db.session.add(token_record)
    db.session.commit()

    reset_url = f"{current_app.config['PUBLIC_APP_URL'].rstrip('/')}/reset-password?{urlencode({'token': token})}"
    try:
        send_password_reset_email(user.email, reset_url)
    except Exception:
        token_record.used_at = now
        db.session.commit()
        logger.exception("Password reset email delivery failed for configured provider.")


def confirm_password_reset(token: str | None, new_password: str, now: float | None = None) -> None:
    """Consume a valid reset token and revoke every existing session."""
    if not isinstance(token, str) or not token or not isinstance(new_password, str):
        raise ValidationError("The reset link is invalid or expired.")
    if len(new_password) < 8 or len(new_password) > 128:
        raise ValidationError("Password must contain 8 to 128 characters.")

    now = time.time() if now is None else now
    token_record = PasswordResetToken.query.filter_by(token_hash=_hash_token(token)).first()
    if token_record is None or token_record.used_at is not None or token_record.expires_at <= now:
        raise ValidationError("The reset link is invalid or expired.")

    user = db.session.get(User, token_record.user_id)
    if user is None or not user.is_active:
        raise ValidationError("The reset link is invalid or expired.")
    user.set_password(new_password)
    user.session_version += 1
    token_record.used_at = now
    PasswordResetToken.query.filter(
        PasswordResetToken.user_id == user.id,
        PasswordResetToken.id != token_record.id,
        PasswordResetToken.used_at.is_(None),
    ).update({"used_at": now})
    db.session.commit()


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
