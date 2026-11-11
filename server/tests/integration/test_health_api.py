"""
Health and readiness API integration tests.
Owner: Akash Pawar (PES2UG24CS041)
Sprint: S1 (S1-09)

Tests implemented (LIVE):
  - test_health_endpoint: GET /api/health returns 200 + expected body
  - test_ready_endpoint: GET /api/ready returns 200 + db ok
  - test_db_isolation: asserts test DB is NOT the developer's database

Tests pending (will be enabled when features are implemented).
"""

import os


class TestHealthEndpoint:
    """TC-Foundation-01: Health endpoint is always live."""

    def test_health_endpoint_returns_200(self, client):
        """GET /api/health must return 200 with correct body."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "ok"
        assert data["service"] == "task-manager-api"

    def test_health_endpoint_no_auth_required(self, client):
        """Health check must be accessible without authentication."""
        response = client.get("/api/health")
        assert response.status_code == 200

    def test_health_content_type_is_json(self, client):
        """Response must be JSON."""
        response = client.get("/api/health")
        assert "application/json" in response.content_type


class TestReadyEndpoint:
    """TC-Foundation-02: Readiness endpoint checks DB."""

    def test_ready_endpoint_returns_200(self, client):
        """GET /api/ready must return 200 when DB is accessible."""
        response = client.get("/api/ready")
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True

    def test_ready_response_format(self, client):
        """Response must follow the standard success envelope."""
        response = client.get("/api/ready")
        data = response.get_json()
        assert "success" in data
        assert "data" in data
        assert "message" in data


class TestDbIsolation:
    """TC-Foundation-03: Test DB must be isolated from developer DB."""

    def test_db_not_developer_database(self, app):
        """
        CRITICAL: Test suite must never use the developer's SQLite file.
        Assert that the test DB URI does not point to the production/dev file.
        """
        uri = app.config["SQLALCHEMY_DATABASE_URI"]
        # Must be a test temp file or in-memory — never the project instance DB
        assert "task_manager.sqlite" not in uri, (
            "CRITICAL: Test suite is using the developer's database! " f"Current URI: {uri}"
        )
        # Must not point to any persistent project path
        project_instance = os.path.join("instance", "task_manager.sqlite")
        assert project_instance.replace("\\", "/") not in uri.replace(
            "\\", "/"
        ), f"Test DB URI points to production database: {uri}"

    def test_test_config_flag(self, app):
        """TESTING flag must be True in test environment."""
        assert app.config["TESTING"] is True

    def test_csrf_disabled_in_tests(self, app):
        """CSRF must be disabled in tests for API calls to work."""
        assert app.config.get("WTF_CSRF_ENABLED") is False


class TestErrorHandlers:
    """TC-Foundation-04: Centralized error handlers return JSON."""

    def test_404_returns_json(self, client):
        """Unknown routes must return JSON 404, not HTML."""
        response = client.get("/api/this-route-does-not-exist")
        assert response.status_code == 404
        data = response.get_json()
        assert data is not None
        assert data["success"] is False
        assert data["error"]["code"] == "NOT_FOUND"

    def test_405_returns_json(self, client):
        """Wrong HTTP method must return JSON 405."""
        response = client.post("/api/health")
        assert response.status_code == 405
        data = response.get_json()
        assert data is not None
        assert data["success"] is False


class TestCsrfEndpoint:
    """TC-Foundation-05: CSRF endpoint is live as part of security foundation."""

    def test_csrf_endpoint_returns_token(self, client):
        """GET /api/auth/csrf must return a token."""
        response = client.get("/api/auth/csrf")
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert "csrf_token" in data["data"]
        assert len(data["data"]["csrf_token"]) > 0
