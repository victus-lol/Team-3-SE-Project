"""
Auth API integration tests.
Owner: Balaji Gowda S R (PES2UG25CS804)
Sprint: S1 (S1-03)
Requirement IDs: TMA-F-001, TMA-F-002
"""

import pytest


class TestLoginEndpoint:
    @pytest.mark.skip(reason="Pending implementation: S1-03")
    def test_login_valid_credentials(self, client, test_user):
        """
        TC-Auth-01 | Owner: Balaji | Requirement: TMA-F-001 | Backlog: S1-03
        POST /api/auth/login with valid credentials returns 200 and user data.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S1-03")
    def test_login_invalid_credentials(self, client, test_user):
        """
        TC-Auth-02 | Owner: Balaji | Requirement: TMA-F-001 | Backlog: S1-03
        POST /api/auth/login with wrong password returns 401.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S1-03")
    def test_login_unknown_email(self, client):
        """
        TC-Auth-02 | Owner: Balaji | Requirement: TMA-F-001 | Backlog: S1-03
        POST /api/auth/login with unknown email returns 401.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S1-03")
    def test_login_missing_fields(self, client):
        """
        Owner: Balaji | Requirement: TMA-F-001 | Backlog: S1-03
        POST /api/auth/login with missing body returns 400.
        """
        pass


class TestLogoutEndpoint:
    @pytest.mark.skip(reason="Pending implementation: S1-03")
    def test_logout_clears_session(self, auth_client):
        """
        TC-Auth-03 | Owner: Balaji | Requirement: TMA-F-002 | Backlog: S1-03
        POST /api/auth/logout returns 200 and clears session.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S1-03")
    def test_protected_route_after_logout_rejected(self, auth_client):
        """
        TC-Auth-03 | Owner: Balaji | Requirement: TMA-F-002 | Backlog: S1-03
        After logout, accessing protected route returns 401.
        """
        pass


class TestMeEndpoint:
    @pytest.mark.skip(reason="Pending implementation: S1-03")
    def test_me_returns_current_user(self, auth_client, test_user):
        """
        Owner: Balaji | Requirement: TMA-F-001 | Backlog: S1-03
        GET /api/auth/me returns current user data.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S1-03")
    def test_me_unauthenticated_returns_401(self, client):
        """
        TC-Sec-01 | Owner: Balaji | Requirement: TMA-SR-001 | Backlog: S1-03
        GET /api/auth/me without session returns 401.
        """
        pass

