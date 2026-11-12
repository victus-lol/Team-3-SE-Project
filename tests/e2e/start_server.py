"""
Start an isolated Flask application for Playwright E2E tests.

This process owns a temporary SQLite database and seeds non-production test
accounts. It never uses or modifies the developer's regular SQLite database.
"""

import os
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SERVER_DIR = PROJECT_ROOT / "server"
sys.path.insert(0, str(SERVER_DIR))

from app import create_app
from app.config import TestingConfig, config_map
from app.extensions import db
from app.models.notification import Notification
from app.models.user import User


_temp_db = tempfile.NamedTemporaryFile(
    prefix="task_manager_e2e_",
    suffix=".sqlite",
    delete=False,
)
DB_PATH = Path(_temp_db.name)
_temp_db.close()


class E2EConfig(TestingConfig):
    """Testing configuration backed by a per-run temporary SQLite file."""

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH.as_posix()}"
    SECRET_KEY = "e2e-only-secret-not-for-production"
    WTF_CSRF_ENABLED = False
    TESTING = True


# Register only inside this short-lived test server process.
config_map["e2e"] = E2EConfig
app = create_app("e2e")


def seed_user(name: str, email: str, password: str, role: str = "user") -> None:
    """Create a test account only when it is not already present."""
    existing = User.query.filter_by(email=email).first()
    if existing is None:
        db.session.add(
            User.create(name=name, email=email, password=password, role=role)
        )


def initialize_database() -> None:
    """Create the schema and deterministic accounts for browser tests."""
    with app.app_context():
        db.create_all()
        seed_user(
            name="E2E Test User",
            email="e2e.user@example.com",
            password="password123",
        )
        seed_user(
            name="E2E Test Admin",
            email="e2e.admin@example.com",
            password="adminpassword123",
            role="admin",
        )
        e2e_user = User.query.filter_by(email="e2e.user@example.com").first()
        if not Notification.query.filter_by(
            user_id=e2e_user.id,
            message="E2E reminder for notification workflow",
        ).first():
            db.session.add(
                Notification(
                    user_id=e2e_user.id,
                    message="E2E reminder for notification workflow",
                    status="pending",
                )
            )
        if not Notification.query.filter_by(
            user_id=e2e_user.id,
            message="E2E unread reminder for read-state workflow",
        ).first():
            db.session.add(
                Notification(
                    user_id=e2e_user.id,
                    message="E2E unread reminder for read-state workflow",
                    status="pending",
                )
            )
        db.session.commit()

    print("E2E database initialized with isolated test user accounts.")


def cleanup_database() -> None:
    """Dispose SQLite connections and remove the temporary database files."""
    with app.app_context():
        db.session.remove()
        db.engine.dispose()

    for path in (
        DB_PATH,
        Path(f"{DB_PATH}-wal"),
        Path(f"{DB_PATH}-shm"),
        Path(f"{DB_PATH}-journal"),
    ):
        try:
            path.unlink(missing_ok=True)
        except OSError as exc:
            print(f"Warning: could not remove temporary database file {path}: {exc}")


if __name__ == "__main__":
    initialize_database()
    try:
        app.run(
            host=os.environ.get("FLASK_HOST", "127.0.0.1"),
            port=int(os.environ.get("FLASK_PORT", "5000")),
            debug=False,
            use_reloader=False,
            threaded=True,
        )
    finally:
        cleanup_database()
