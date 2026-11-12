"""Persistent login throttling state; account and address values are hashed."""

from ..extensions import db


class LoginAttempt(db.Model):
    __tablename__ = "login_attempts"

    key_hash = db.Column(db.String(64), primary_key=True)
    failure_count = db.Column(db.Integer, nullable=False, default=0)
    window_started_at = db.Column(db.Float, nullable=False)
    locked_until = db.Column(db.Float, nullable=True)
