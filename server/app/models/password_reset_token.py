"""Single-use, hashed password reset tokens."""

from ..extensions import db


class PasswordResetToken(db.Model):
    __tablename__ = "password_reset_tokens"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash = db.Column(db.String(64), nullable=False, unique=True, index=True)
    expires_at = db.Column(db.Float, nullable=False, index=True)
    used_at = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.Float, nullable=False)
