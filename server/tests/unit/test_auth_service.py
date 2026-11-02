
import pytest

from app.auth.service import authenticate, create_admin_user
from app.common.exceptions import AuthenticationError, ConflictError


class TestAuthService:

    def test_authenticate_valid_credentials(self, db, test_user):
        user = authenticate("testuser@example.com", "password123")

        assert user.id == test_user.id
        assert user.email == "testuser@example.com"

    def test_authenticate_invalid_password(self, db, test_user):
        with pytest.raises(AuthenticationError):
            authenticate("testuser@example.com", "wrongpassword")

    def test_authenticate_unknown_email(self, db):
        with pytest.raises(AuthenticationError):
            authenticate("unknown@example.com", "password123")

    def test_create_admin_user(self, db):
        admin = create_admin_user(
            name="Test Admin",
            email="newadmin@example.com",
            password="adminpass123",
        )

        assert admin.role == "admin"
        assert admin.email == "newadmin@example.com"
        assert admin.check_password("adminpass123")

    def test_create_admin_duplicate_email_rejected(self, db, test_admin):
        with pytest.raises(ConflictError):
            create_admin_user(
                name="Another Admin",
                email=test_admin.email,
                password="anotherpass123",
            )
