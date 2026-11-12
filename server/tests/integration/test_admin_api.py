"""
Admin API integration tests.
Owner: Balaji Gowda S R (PES2UG25CS804)
Sprint: S2 (S2-06)
Requirement IDs: TMA-SR-001, TMA-SR-003
"""

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

    def test_audit_logs_unauthenticated_returns_401(self, client):
        assert client.get("/api/admin/audit-logs").status_code == 401

    def test_audit_logs_standard_user_returns_403(self, auth_client):
        assert auth_client.get("/api/admin/audit-logs").status_code == 403


class TestAdminApi:
    def test_admin_list_users(self, admin_client):
        """
        TC-Admin-01 | Owner: Balaji | Requirement: TMA-SR-001 | Backlog: S2-06
        GET /api/admin/users with admin session returns user list.
        """
        response = admin_client.get("/api/admin/users")

        assert response.status_code == 200
        users = response.get_json()["data"]
        assert any(user["email"] == "testadmin@example.com" for user in users)

    def test_admin_response_excludes_password_hashes(self, admin_client):
        """
        TC-Sec-03 | Owner: Balaji | Requirement: TMA-SR-003 | Backlog: S2-06
        Admin user listing never includes password_hash in response.
        """
        response = admin_client.get("/api/admin/users")

        assert response.status_code == 200
        assert all("password_hash" not in user for user in response.get_json()["data"])

    def test_admin_user_listing_writes_secret_free_audit_event(self, admin_client, test_admin, db):
        from app.models.audit_log import AuditLog

        assert admin_client.get("/api/admin/users").status_code == 200
        event = AuditLog.query.one()
        assert event.actor_id == test_admin.id
        assert event.action == "admin.users.listed"
        assert event.to_dict().keys() == {
            "id", "actor_id", "action", "target_type", "target_id", "created_at"
        }
        assert "password" not in str(event.to_dict()).lower()

    def test_admin_can_list_audit_logs_with_pagination(self, admin_client):
        admin_client.get("/api/admin/users")
        response = admin_client.get("/api/admin/audit-logs?page=1&per_page=10")

        assert response.status_code == 200
        assert response.get_json()["data"][0]["action"] == "admin.users.listed"
        assert response.get_json()["pagination"]["total_items"] >= 1
