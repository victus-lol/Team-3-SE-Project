"""
Model unit tests.
Owner: Each model owner; coordinated by Aadi Kore (PES2UG24CS006) as QA lead.
Sprint: S1 (S1-09)

Tests model creation, constraints, relationships, FK enforcement,
and invalid status/priority rejection.

All tests in this file are LIVE (no pending markers) — models are implemented.
"""

import pytest
from sqlalchemy.exc import IntegrityError

from app.models.category import Category
from app.models.notification import Notification
from app.models.task import Task
from app.models.user import User


class TestUserModel:
    """Tests for the User model (Balaji)."""

    def test_create_user(self, db):
        """User.create() produces a valid user with hashed password."""
        user = User.create(name="Alice", email="alice@example.com", password="password123")
        db.session.add(user)
        db.session.commit()
        assert user.id is not None
        assert user.email == "alice@example.com"
        assert user.role == "user"
        assert user.password_hash != "password123"

    def test_email_normalized_to_lowercase(self, db):
        """Email must be stored lowercase and stripped."""
        user = User.create(name="Bob", email="  BOB@Example.COM  ", password="password123")
        db.session.add(user)
        db.session.commit()
        assert user.email == "bob@example.com"

    def test_password_check(self, db):
        """check_password() returns True for matching password."""
        user = User.create(name="Carol", email="carol@example.com", password="securepass")
        assert user.check_password("securepass") is True
        assert user.check_password("wrongpass") is False

    def test_password_not_stored_in_plaintext(self, db):
        """password_hash must never equal the plaintext password."""
        user = User.create(name="Dan", email="dan@example.com", password="mypassword")
        assert user.password_hash != "mypassword"
        assert len(user.password_hash) > 0

    def test_unique_email_constraint(self, db):
        """Duplicate email must raise IntegrityError."""
        user1 = User.create(name="Eve", email="eve@example.com", password="password123")
        user2 = User.create(name="Eve2", email="eve@example.com", password="password456")
        db.session.add(user1)
        db.session.commit()
        db.session.add(user2)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

    def test_role_default_is_user(self, db):
        """Default role must be 'user'."""
        user = User.create(name="Frank", email="frank@example.com", password="password123")
        db.session.add(user)
        db.session.commit()
        assert user.role == "user"

    def test_public_create_cannot_set_admin(self):
        """User.create() must reject invalid roles."""
        with pytest.raises(ValueError, match="role must be"):
            User.create(name="Hacker", email="h@x.com", password="password123", role="superuser")

    def test_to_dict_excludes_password_hash(self, db):
        """to_dict() must never include password_hash."""
        user = User.create(name="Grace", email="grace@example.com", password="password123")
        db.session.add(user)
        db.session.commit()
        d = user.to_dict()
        assert "password_hash" not in d
        assert "email" in d

    def test_is_active_default_true(self, db):
        """is_active defaults to True."""
        user = User.create(name="Hank", email="hank@example.com", password="password123")
        db.session.add(user)
        db.session.commit()
        assert user.is_active is True

    def test_short_password_rejected(self):
        """Password shorter than 8 chars must raise ValueError."""
        with pytest.raises(ValueError, match="at least 8"):
            User.create(name="Ivan", email="ivan@example.com", password="short")


class TestTaskModel:
    """Tests for the Task model (Aadi)."""

    def test_create_task(self, db, test_user):
        """Task creation with valid fields succeeds."""
        task = Task(owner_id=test_user.id, title="My Task", priority="high", status="pending")
        db.session.add(task)
        db.session.commit()
        assert task.id is not None
        assert task.title == "My Task"
        assert task.owner_id == test_user.id

    def test_task_default_priority_medium(self, db, test_user):
        """Default priority is 'medium'."""
        task = Task(owner_id=test_user.id, title="Task Defaults")
        db.session.add(task)
        db.session.commit()
        assert task.priority == "medium"

    def test_task_default_status_pending(self, db, test_user):
        """Default status is 'pending'."""
        task = Task(owner_id=test_user.id, title="Pending Task")
        db.session.add(task)
        db.session.commit()
        assert task.status == "pending"

    def test_task_owner_relationship(self, db, test_user):
        """task.owner should return the User."""
        task = Task(owner_id=test_user.id, title="Owned Task")
        db.session.add(task)
        db.session.commit()
        assert task.owner.id == test_user.id

    def test_task_cascades_delete_with_user(self, db):
        """Deleting a user must cascade-delete their tasks (FK CASCADE)."""
        user = User.create(name="TempUser", email="tmp@example.com", password="password123")
        db.session.add(user)
        db.session.commit()
        task = Task(owner_id=user.id, title="To be deleted")
        db.session.add(task)
        db.session.commit()
        task_id = task.id
        db.session.delete(user)
        db.session.commit()
        assert Task.query.get(task_id) is None

    def test_task_requires_title(self, db, test_user):
        """Task without title must fail."""
        task = Task(owner_id=test_user.id, title=None)
        db.session.add(task)
        with pytest.raises(Exception):
            db.session.commit()
        db.session.rollback()

    def test_task_to_dict(self, db, sample_task):
        """to_dict() includes required keys."""
        d = sample_task.to_dict()
        for key in ("id", "owner_id", "title", "priority", "status"):
            assert key in d


class TestCategoryModel:
    """Tests for the Category model (Aadi)."""

    def test_create_category(self, db, test_user):
        """Category.create() normalizes name to lowercase."""
        cat = Category.create(user_id=test_user.id, name="Work")
        db.session.add(cat)
        db.session.commit()
        assert cat.name == "work"
        assert cat.user_id == test_user.id

    def test_category_unique_per_user(self, db, test_user):
        """Same name for same user must raise IntegrityError."""
        cat1 = Category.create(user_id=test_user.id, name="personal")
        cat2 = Category.create(user_id=test_user.id, name="personal")
        db.session.add(cat1)
        db.session.commit()
        db.session.add(cat2)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

    def test_same_name_different_users_allowed(self, db, test_user, test_admin):
        """Same category name for different users is allowed."""
        cat1 = Category.create(user_id=test_user.id, name="shared")
        cat2 = Category.create(user_id=test_admin.id, name="shared")
        db.session.add_all([cat1, cat2])
        db.session.commit()
        assert cat1.id != cat2.id

    def test_empty_category_name_rejected(self):
        """Empty category name must raise ValueError."""
        with pytest.raises(ValueError, match="empty"):
            Category.create(user_id=1, name="   ")

    def test_category_user_relationship(self, db, test_user):
        """category.user returns the owning User."""
        cat = Category.create(user_id=test_user.id, name="hobbies")
        db.session.add(cat)
        db.session.commit()
        assert cat.user.id == test_user.id


class TestNotificationModel:
    """Tests for the Notification model (Akash)."""

    def test_create_notification(self, db, test_user):
        """Notification creation with valid fields succeeds."""
        notif = Notification(
            user_id=test_user.id,
            message="Task is due soon.",
            status="pending",
        )
        db.session.add(notif)
        db.session.commit()
        assert notif.id is not None
        assert notif.status == "pending"

    def test_notification_status_default_pending(self, db, test_user):
        """Default status is 'pending'."""
        notif = Notification(user_id=test_user.id, message="Hello")
        db.session.add(notif)
        db.session.commit()
        assert notif.status == "pending"

    def test_notification_requires_message(self, db, test_user):
        """Notification without message must fail."""
        notif = Notification(user_id=test_user.id, message=None)
        db.session.add(notif)
        with pytest.raises(Exception):
            db.session.commit()
        db.session.rollback()

    def test_notification_user_relationship(self, db, test_user):
        """notification.user returns the User."""
        notif = Notification(user_id=test_user.id, message="Test")
        db.session.add(notif)
        db.session.commit()
        assert notif.user.id == test_user.id

    def test_notification_cascades_with_user(self, db):
        """Deleting user must cascade-delete their notifications."""
        user = User.create(name="NotifUser", email="nu@example.com", password="password123")
        db.session.add(user)
        db.session.commit()
        notif = Notification(user_id=user.id, message="Will be deleted")
        db.session.add(notif)
        db.session.commit()
        notif_id = notif.id
        db.session.delete(user)
        db.session.commit()
        assert Notification.query.get(notif_id) is None


class TestForeignKeyEnforcement:
    """TC-Sec-05: FK constraints must be enforced at DB level."""

    def test_task_requires_valid_owner(self, db):
        """Task with non-existent owner_id must fail FK check."""
        task = Task(owner_id=99999, title="Orphan Task")
        db.session.add(task)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

    def test_notification_requires_valid_user(self, db):
        """Notification with non-existent user_id must fail FK check."""
        notif = Notification(user_id=99999, message="Orphan")
        db.session.add(notif)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

