"""
Shared test fixtures for all pytest test suites.
Owner: Akash Pawar (PES2UG24CS041)
Sprint: S1 (S1-09)

Fixtures provided:
  - app          : Flask test application (in-memory SQLite, isolated from dev DB)
  - client       : Flask test client
  - db_session   : database session scoped to each test (tables reset per test)
  - test_user    : a regular authenticated User
  - test_admin   : an admin User
  - auth_client  : test client with test_user logged in (session authenticated)
  - admin_client : test client with test_admin logged in
  - sample_task  : a Task owned by test_user
  - sample_category : a Category owned by test_user
  - fake_provider: FakeNotificationProvider instance

CRITICAL:
  The test app MUST use a separate, temporary SQLite DB.
  It MUST NOT touch the developer's database.
  This is asserted in test_health_api.py::test_db_isolation.
"""

import os
import tempfile

import pytest

from app import create_app
from app.extensions import db as _db
from app.models.audit_log import AuditLog
from app.models.category import Category
from app.models.login_attempt import LoginAttempt
from app.models.notification import Notification
from app.models.password_reset_token import PasswordResetToken
from app.models.task import Task
from app.models.user import User
from app.notifications.provider import FakeNotificationProvider


@pytest.fixture(scope="session")
def app():
    """
    Create the Flask app configured for testing.
    Uses an isolated temporary SQLite file (not in-memory) so that FK
    enforcement via WAL works. The temp file is deleted after the session.
    """
    db_fd, db_path = tempfile.mkstemp(suffix=".sqlite", prefix="test_taskmanager_")
    os.close(db_fd)

    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        "WTF_CSRF_ENABLED": False,
        "WTF_CSRF_METHODS": [],
        "SECRET_KEY": "test-secret-key-not-for-production",
        "SERVER_NAME": "localhost",
        "LOGIN_DISABLED": False,
    }

    app = create_app("testing")
    app.config.update(test_config)

    with app.app_context():
        _db.create_all()

    yield app

    # Teardown: remove temp DB
    with app.app_context():
        _db.drop_all()
    os.unlink(db_path)


@pytest.fixture(scope="session")
def db(app):
    """Provide the database instance for the test session."""
    return _db


@pytest.fixture
def app_context(app):
    """Provide an application context for database operations."""
    with app.app_context():
        yield


@pytest.fixture(autouse=True)
def clean_db(db, app_context):
    """
    Reset database state between tests by rolling back and clearing tables.
    This ensures test isolation without recreating the schema each time.
    """
    yield
    db.session.remove()
    # Delete in FK-safe order
    db.session.execute(Notification.__table__.delete())
    db.session.execute(AuditLog.__table__.delete())
    db.session.execute(PasswordResetToken.__table__.delete())
    db.session.execute(LoginAttempt.__table__.delete())
    db.session.execute(Task.__table__.delete())
    db.session.execute(Category.__table__.delete())
    db.session.execute(User.__table__.delete())
    db.session.commit()


@pytest.fixture
def client(app):
    """Flask test client — unauthenticated."""
    return app.test_client()


@pytest.fixture
def test_user(db):
    """Create and persist a regular test user."""
    user = User.create(
        name="Test User",
        email="testuser@example.com",
        password="password123",
        role="user",
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def test_admin(db):
    """Create and persist an admin test user."""
    admin = User.create(
        name="Test Admin",
        email="testadmin@example.com",
        password="adminpass123",
        role="admin",
    )
    db.session.add(admin)
    db.session.commit()
    return admin


@pytest.fixture
def auth_client(app, test_user):
    """
    Test client with test_user logged in via Flask-Login.
    Uses the test client context to simulate a session.
    """
    client = app.test_client()
    with client.session_transaction() as sess:
        sess["_user_id"] = str(test_user.id)
        sess["_fresh"] = True
    return client


@pytest.fixture
def admin_client(app, test_admin):
    """Test client with test_admin logged in."""
    client = app.test_client()
    with client.session_transaction() as sess:
        sess["_user_id"] = str(test_admin.id)
        sess["_fresh"] = True
    return client


@pytest.fixture
def sample_category(db, test_user):
    """Create a Category owned by test_user."""
    cat = Category.create(user_id=test_user.id, name="work")
    db.session.add(cat)
    db.session.commit()
    return cat


@pytest.fixture
def sample_task(db, test_user, sample_category):
    """Create a Task owned by test_user."""
    task = Task(
        owner_id=test_user.id,
        title="Sample Task",
        description="A sample task for testing.",
        priority="medium",
        status="pending",
        category_id=sample_category.id,
    )
    db.session.add(task)
    db.session.commit()
    return task


@pytest.fixture
def fake_provider():
    """FakeNotificationProvider — use in notification tests."""
    provider = FakeNotificationProvider()
    return provider
