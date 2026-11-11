"""
Admin API integration tests.
Owner: Balaji Gowda S R (PES2UG25CS804)
Sprint: S2 (S2-06)
Requirement IDs: TMA-SR-001, TMA-SR-003
"""

import pytest


class TestAdminApiLive:
    def test_admin_users_unauthenticated_returns_401(self, client):
        """
        TC-Admin-01 | Owner: Balaji | Requirement: TMA-SR-001 | Backlog: S2-06
        GET /api/admin/users without auth returns 401.
        """
        response = client.get("/api/admin/users")
        assert response.status_code == 401

    def test_admin_users_standard_user_returns_403(self, auth_client):
        """
        TC-Admin-01 | Owner: Balaji | Requirement: TMA-SR-001 | Backlog: S2-06
        GET /api/admin/users with standard user session returns 403.
        This test is LIVE — the admin_required decorator is implemented.
        """
        response = auth_client.get("/api/admin/users")
        assert response.status_code == 403
        data = response.get_json()
        assert data["success"] is False
        assert data["error"]["code"] == "AUTHORIZATION_ERROR"


class TestAdminApi:
    @pytest.mark.skip(reason="Pending implementation: S2-06")
    def test_admin_list_users(self, admin_client):
        """
        TC-Admin-01 | Owner: Balaji | Requirement: TMA-SR-001 | Backlog: S2-06
        GET /api/admin/users with admin session returns user list.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-06")
    def test_admin_response_excludes_password_hashes(self, admin_client):
        """
        TC-Sec-03 | Owner: Balaji | Requirement: TMA-SR-003 | Backlog: S2-06
        Admin user listing never includes password_hash in response.
        """
        pass
