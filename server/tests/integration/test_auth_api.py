


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
