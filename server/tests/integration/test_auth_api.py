import pytest

from app.common.exceptions import ValidationError


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


class TestPasswordResetEndpoints:
    def test_request_response_does_not_disclose_account_existence(self, client, test_user, monkeypatch):
        from app.auth import password_reset

        sent = []
        monkeypatch.setattr(password_reset, "send_password_reset_email", lambda email, url: sent.append((email, url)))

        known = client.post("/api/auth/password-reset/request", json={"email": test_user.email})
        unknown = client.post("/api/auth/password-reset/request", json={"email": "missing@example.com"})

        assert known.status_code == unknown.status_code == 202
        assert known.get_json() == unknown.get_json()
        assert sent[0][0] == test_user.email
        assert "token=" in sent[0][1]

    def test_reset_token_is_single_use_and_revokes_existing_sessions(
        self, client, test_user, monkeypatch
    ):
        from urllib.parse import parse_qs, urlparse

        from app.auth import password_reset
        from app.models.password_reset_token import PasswordResetToken

        sent = []
        monkeypatch.setattr(password_reset, "send_password_reset_email", lambda email, url: sent.append(url))
        assert client.post(
            "/api/auth/login",
            json={"email": test_user.email, "password": "password123"},
        ).status_code == 200
        with client.session_transaction() as session_data:
            assert session_data.get("_auth_version") == 0
        assert client.post(
            "/api/auth/password-reset/request",
            json={"email": test_user.email},
        ).status_code == 202
        token = parse_qs(urlparse(sent[0]).query)["token"][0]
        stored_token = PasswordResetToken.query.one()
        assert stored_token.token_hash != token

        response = client.post(
            "/api/auth/password-reset/confirm",
            json={"token": token, "password": "newpassword123"},
        )

        assert response.status_code == 200
        assert test_user.session_version == 1
        with client.session_transaction() as session_data:
            assert session_data.get("_auth_version") == 0
        # The session-scoped fixture keeps one Flask app context across requests.
        # Clear its cached current_user to model a fresh request after reset.
        from flask import g

        g.pop("_login_user", None)
        assert client.get("/api/auth/me").status_code == 401
        assert test_user.check_password("newpassword123")
        assert client.post(
            "/api/auth/password-reset/confirm",
            json={"token": token, "password": "anotherpassword"},
        ).status_code == 400
        assert client.post(
            "/api/auth/login",
            json={"email": test_user.email, "password": "newpassword123"},
        ).status_code == 200

    def test_invalid_expired_and_used_tokens_are_rejected(self, app, test_user, db):
        from app.auth.password_reset import _hash_token, confirm_password_reset
        from app.models.password_reset_token import PasswordResetToken

        expired = PasswordResetToken(
            user_id=test_user.id,
            token_hash=_hash_token("expired"),
            created_at=100,
            expires_at=150,
        )
        db.session.add(expired)
        db.session.commit()

        with app.app_context(), pytest.raises(ValidationError):
            confirm_password_reset("expired", "newpassword123", now=151)
        with app.app_context(), pytest.raises(ValidationError):
            confirm_password_reset("unknown", "newpassword123", now=151)

    def test_password_reset_requires_valid_password(self, client):
        response = client.post(
            "/api/auth/password-reset/confirm",
            json={"token": "unknown", "password": "short"},
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
