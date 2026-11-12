class TestLoginEndpoint:
    def test_login_valid_credentials(self, client, test_user):
        response = client.post(
            "/api/auth/login",
            json={
                "email": "testuser@example.com",
                "password": "password123",
            },
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert data["data"]["email"] == test_user.email
        assert "password_hash" not in data["data"]

    def test_login_invalid_credentials(self, client, test_user):
        response = client.post(
            "/api/auth/login",
            json={
                "email": "testuser@example.com",
                "password": "wrongpassword",
            },
        )

        assert response.status_code == 401
        assert client.get("/api/auth/me").status_code == 401

    def test_login_unknown_email(self, client):
        response = client.post(
            "/api/auth/login",
            json={
                "email": "unknown@example.com",
                "password": "password123",
            },
        )

        assert response.status_code == 401
        assert client.get("/api/auth/me").status_code == 401

    def test_login_missing_fields(self, client):
        response = client.post("/api/auth/login", json={})

        assert response.status_code == 400


class TestLogoutEndpoint:
    def test_logout_clears_session(self, auth_client):
        response = auth_client.post("/api/auth/logout")

        assert response.status_code == 200
        assert response.get_json()["success"] is True

    def test_protected_route_after_logout_rejected(self, auth_client):
        auth_client.post("/api/auth/logout")

        response = auth_client.get("/api/auth/me")

        assert response.status_code == 401


class TestMeEndpoint:
    def test_me_returns_current_user(self, auth_client, test_user):
        response = auth_client.get("/api/auth/me")

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert data["data"]["email"] == test_user.email
        assert "password_hash" not in data["data"]

    def test_me_unauthenticated_returns_401(self, client):
        response = client.get("/api/auth/me")

        assert response.status_code == 401

    def test_me_updates_only_display_name(self, auth_client, test_user):
        response = auth_client.patch("/api/auth/me", json={"name": "  Updated Name  "})

        assert response.status_code == 200
        assert response.get_json()["data"]["name"] == "Updated Name"
        assert test_user.name == "Updated Name"
        assert "password_hash" not in response.get_json()["data"]

    def test_me_rejects_protected_profile_fields(self, auth_client, test_user):
        response = auth_client.patch("/api/auth/me", json={"role": "admin", "name": "Changed"})

        assert response.status_code == 400
        assert test_user.role == "user"
        assert test_user.name == "Test User"

    def test_me_update_requires_authentication(self, client):
        assert client.patch("/api/auth/me", json={"name": "Updated"}).status_code == 401


class TestRegistrationEndpoint:
    def test_register_creates_standard_user(self, client):
        response = client.post(
            "/api/auth/register",
            json={
                "name": "  New User  ",
                "email": "New.User@example.com",
                "password": "securepass123",
                "role": "admin",
            },
        )

        assert response.status_code == 201
        user = response.get_json()["data"]
        assert user["name"] == "New User"
        assert user["email"] == "new.user@example.com"
        assert user["role"] == "user"
        assert "password_hash" not in user

    def test_register_rejects_duplicate_email_case_insensitively(self, client, test_user):
        response = client.post(
            "/api/auth/register",
            json={"name": "Another User", "email": test_user.email.upper(), "password": "securepass123"},
        )

        assert response.status_code == 409

    def test_register_rejects_invalid_input(self, client):
        response = client.post(
            "/api/auth/register",
            json={"name": " ", "email": "not-an-email", "password": "short"},
        )

        assert response.status_code == 400


class TestLoginThrottle:
    def test_repeated_failures_are_temporarily_locked(self, app, client, test_user, monkeypatch):
        monkeypatch.setitem(app.config, "LOGIN_MAX_ATTEMPTS", 2)
        monkeypatch.setitem(app.config, "LOGIN_LOCKOUT_SECONDS", 60)
        credentials = {"email": test_user.email, "password": "incorrectpass"}

        assert client.post("/api/auth/login", json=credentials).status_code == 401
        assert client.post("/api/auth/login", json=credentials).status_code == 401
        response = client.post("/api/auth/login", json={"email": test_user.email, "password": "password123"})

        assert response.status_code == 429
        assert response.get_json()["error"]["code"] == "RATE_LIMITED"

    def test_lockout_expires_after_configured_cooldown(self, app, monkeypatch):
        from app.auth.throttle import is_login_locked, record_failed_login

        monkeypatch.setitem(app.config, "LOGIN_MAX_ATTEMPTS", 1)
        monkeypatch.setitem(app.config, "LOGIN_LOCKOUT_SECONDS", 60)
        monkeypatch.setitem(app.config, "LOGIN_ATTEMPT_WINDOW_SECONDS", 300)
        record_failed_login("cooldown@example.com", "127.0.0.1", now=1000)

        assert is_login_locked("cooldown@example.com", "127.0.0.1", now=1059)
        assert not is_login_locked("cooldown@example.com", "127.0.0.1", now=1061)

    def test_successful_login_clears_prior_failures(self, app, client, test_user, monkeypatch):
        monkeypatch.setitem(app.config, "LOGIN_MAX_ATTEMPTS", 2)
        client.post("/api/auth/login", json={"email": test_user.email, "password": "incorrectpass"})

        response = client.post("/api/auth/login", json={"email": test_user.email, "password": "password123"})

        assert response.status_code == 200
