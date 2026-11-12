"""SMTP delivery for account recovery messages."""

import smtplib
from email.message import EmailMessage

from flask import current_app


def send_password_reset_email(recipient: str, reset_url: str) -> None:
    """Send a reset link over configured TLS SMTP without logging its token."""
    config = current_app.config
    if not config.get("MAIL_SERVER") or not config.get("MAIL_FROM"):
        raise RuntimeError("Password reset email delivery is not configured.")

    message = EmailMessage()
    message["Subject"] = "Reset your Task Manager password"
    message["From"] = config["MAIL_FROM"]
    message["To"] = recipient
    message.set_content(
        "We received a request to reset your Task Manager password. "
        f"Use this single-use link within {config['PASSWORD_RESET_TOKEN_TTL_SECONDS'] // 60} minutes:\n\n"
        f"{reset_url}\n\nIf you did not request this, you can ignore this email."
    )

    smtp_type = smtplib.SMTP_SSL if config.get("MAIL_USE_SSL") else smtplib.SMTP
    with smtp_type(config["MAIL_SERVER"], config["MAIL_PORT"], timeout=10) as smtp:
        if not config.get("MAIL_USE_SSL"):
            smtp.starttls()
        username = config.get("MAIL_USERNAME")
        password = config.get("MAIL_PASSWORD")
        if username:
            smtp.login(username, password or "")
        smtp.send_message(message)
