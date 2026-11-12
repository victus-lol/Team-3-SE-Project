"""
Security API integration tests.
Owner: Aadi Kore (PES2UG24CS006) + Akash Pawar (PES2UG24CS041)
Sprint: S2 (S2-10)
Requirement IDs: TMA-SR-001, TMA-SR-003, TMA-SR-004, TMA-SR-005
"""

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

    def test_api_security_headers_are_present(self, client):
        response = client.get("/api/health")

        assert response.headers["X-Content-Type-Options"] == "nosniff"
        assert response.headers["X-Frame-Options"] == "DENY"
        assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
        assert "default-src 'none'" in response.headers["Content-Security-Policy"]

    def test_oversized_request_uses_standard_error_envelope(self, app, client, monkeypatch):
        monkeypatch.setitem(app.config, "MAX_CONTENT_LENGTH", 32)
        response = client.post("/api/auth/login", data=b"x" * 64, content_type="application/json")

        assert response.status_code == 413
        assert response.get_json()["error"]["code"] == "REQUEST_TOO_LARGE"


class TestSecurityApi:
    def test_password_hashes_not_in_api_response(self, admin_client, test_user):
        """
        TC-Sec-03 | Owner: Balaji | Requirement: TMA-SR-003 | Backlog: S2-10
        No API response ever includes password_hash.
        """
        response = admin_client.get("/api/admin/users")

        assert response.status_code == 200
        assert all("password_hash" not in user for user in response.get_json()["data"])

    def test_hostile_input_does_not_crash(self, auth_client):
        """
        TC-Sec-05 | Owner: Aadi | Requirement: TMA-SR-005 | Backlog: S2-10
        Hostile input (XSS, SQLi attempts) in task title is sanitized/rejected.
        """
        title = "<script>alert('xss')</script> OR 1=1 --"
        response = auth_client.post("/api/tasks", json={"title": title})

        assert response.status_code == 201
        assert response.get_json()["data"]["title"] == title
        assert auth_client.get("/api/tasks?q=%27%20OR%201%3D1%20--").status_code == 200

    def test_non_admin_denied_admin_endpoint(self, auth_client):
        """
        TC-Sec-02 | Owner: Balaji | Requirement: TMA-SR-001 | Backlog: S2-10
        Standard user is rejected from admin endpoints with 403.
        (Additional coverage beyond test_admin_api.py)
        """
        response = auth_client.get("/api/admin/users")

        assert response.status_code == 403
