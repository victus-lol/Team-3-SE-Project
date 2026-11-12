"""
Security API integration tests.
Owner: Aadi Kore (PES2UG24CS006) + Akash Pawar (PES2UG24CS041)
Sprint: S2 (S2-10)
Requirement IDs: TMA-SR-001, TMA-SR-003, TMA-SR-004, TMA-SR-005
"""

import pytest


class TestSecurityApiLive:
    def test_unauthenticated_task_access_rejected(self, client):
        """
        TC-Sec-01 | Owner: Aadi | Requirement: TMA-SR-001 | Backlog: S2-10
        All task endpoints require authentication (401 when not logged in).
        """
        for endpoint in [
            "/api/tasks",
            "/api/tasks/1",
            "/api/dashboard/summary",
            "/api/notifications",
            "/api/admin/users",
        ]:
            resp = client.get(endpoint)
            assert resp.status_code in (
                401,
                405,
            ), f"Expected 401 for {endpoint}, got {resp.status_code}"

    def test_error_response_never_includes_stack_trace(self, client):
        """
        TC-Sec-05 | Owner: Akash | Requirement: TMA-SR-003 | Backlog: S2-10
        Error responses must not expose stack traces or internal details.
        """
        response = client.get("/api/this-does-not-exist")
        data = response.get_json()
        assert "traceback" not in str(data).lower()
        assert "exception" not in str(data).lower()


class TestSecurityPending:
    @pytest.mark.skip(reason="Pending implementation: S2-10")
    def test_password_hashes_not_in_api_response(self, admin_client, test_user):
        """
        TC-Sec-03 | Owner: Balaji | Requirement: TMA-SR-003 | Backlog: S2-10
        No API response ever includes password_hash.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-10")
    def test_hostile_input_does_not_crash(self, auth_client):
        """
        TC-Sec-05 | Owner: Aadi | Requirement: TMA-SR-005 | Backlog: S2-10
        Hostile input (XSS, SQLi attempts) in task title is sanitized/rejected.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-10")
    def test_non_admin_denied_admin_endpoint(self, auth_client):
        """
        TC-Sec-02 | Owner: Balaji | Requirement: TMA-SR-001 | Backlog: S2-10
        Standard user is rejected from admin endpoints with 403.
        (Additional coverage beyond test_admin_api.py)
        """
        pass
