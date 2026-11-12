"""Database-backed login throttling keyed by hashed email and client address."""

import hashlib
import time

from ..extensions import db
from ..models.login_attempt import LoginAttempt


def _key(email: str | None, client_address: str | None) -> str:
    identity = f"{(email or '').strip().lower()}\0{client_address or 'unknown'}"
    return hashlib.sha256(identity.encode("utf-8")).hexdigest()


def is_login_locked(email: str | None, client_address: str | None, now: float | None = None) -> bool:
    now = time.time() if now is None else now
    key_hash = _key(email, client_address)
    attempt = db.session.get(LoginAttempt, key_hash)
    if attempt is None:
        return False
    if attempt.locked_until and attempt.locked_until > now:
        return True

    window = current_app_window_seconds()
    if now - attempt.window_started_at >= window or attempt.locked_until is not None:
        db.session.delete(attempt)
        db.session.commit()
    return False


def record_failed_login(email: str | None, client_address: str | None, now: float | None = None) -> bool:
    """Record failure and return whether the configured threshold was reached."""
    from flask import current_app

    now = time.time() if now is None else now
    key_hash = _key(email, client_address)
    attempt = db.session.get(LoginAttempt, key_hash)
    window = current_app.config["LOGIN_ATTEMPT_WINDOW_SECONDS"]
    if attempt is None or now - attempt.window_started_at >= window:
        if attempt is not None:
            db.session.delete(attempt)
            db.session.flush()
        attempt = LoginAttempt(key_hash=key_hash, failure_count=0, window_started_at=now)
        db.session.add(attempt)

    attempt.failure_count += 1
    locked = attempt.failure_count >= current_app.config["LOGIN_MAX_ATTEMPTS"]
    if locked:
        attempt.locked_until = now + current_app.config["LOGIN_LOCKOUT_SECONDS"]
    db.session.commit()
    return locked


def clear_login_failures(email: str | None, client_address: str | None) -> None:
    attempt = db.session.get(LoginAttempt, _key(email, client_address))
    if attempt is not None:
        db.session.delete(attempt)
        db.session.commit()


def current_app_window_seconds() -> int:
    from flask import current_app

    return current_app.config["LOGIN_ATTEMPT_WINDOW_SECONDS"]
