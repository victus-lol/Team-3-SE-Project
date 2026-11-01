"""
Auth service unit tests.
Owner: Balaji Gowda S R (PES2UG25CS804)
Sprint: S1 (S1-03)
Requirement IDs: TMA-F-001, TMA-F-002, TMA-SR-001
"""

import pytest


class TestAuthService:
    """Unit tests for server/app/auth/service.py"""

    @pytest.mark.skip(reason="Pending implementation: S1-03")
    def test_authenticate_valid_credentials(self, db, test_user):
        """
        TC-Auth-01 | Owner: Balaji | Requirement: TMA-F-001 | Backlog: S1-03
        authenticate(email, password) returns User on valid credentials.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S1-03")
    def test_authenticate_invalid_password(self, db, test_user):
        """
        TC-Auth-02 | Owner: Balaji | Requirement: TMA-F-001 | Backlog: S1-03
        authenticate() raises AuthenticationError on wrong password.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S1-03")
    def test_authenticate_unknown_email(self, db):
        """
        TC-Auth-02 | Owner: Balaji | Requirement: TMA-F-001 | Backlog: S1-03
        authenticate() raises AuthenticationError on unknown email.
        Error message must not reveal which field is wrong.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S1-03")
    def test_create_admin_user(self, db):
        """
        Owner: Balaji | Requirement: TMA-SR-001 | Backlog: S1-03
        create_admin_user() creates a user with role='admin'.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S1-03")
    def test_create_admin_duplicate_email_rejected(self, db, test_admin):
        """
        Owner: Balaji | Requirement: TMA-SR-001 | Backlog: S1-03
        create_admin_user() raises ConflictError on duplicate email.
        """
        pass

