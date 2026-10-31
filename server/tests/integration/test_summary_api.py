"""
Dashboard summary API integration tests.
Owner: Balaji Gowda S R (PES2UG25CS804)
Sprint: S2 (S2-04)
Requirement IDs: TMA-F-033
"""

import pytest


class TestDashboardApiLive:
    def test_summary_unauthenticated_returns_401(self, client):
        """
        TC-Sec-01 | Owner: Balaji | Requirement: TMA-SR-001 | Backlog: S2-04
        GET /api/dashboard/summary without auth returns 401.
        """
        response = client.get("/api/dashboard/summary")
        assert response.status_code == 401


class TestDashboardApi:
    @pytest.mark.skip(reason="Pending implementation: S2-04")
    def test_summary_returns_counts(self, auth_client, db, test_user):
        """
        TC-Summary-01 | Owner: Balaji | Requirement: TMA-F-033 | Backlog: S2-04
        GET /api/dashboard/summary returns pending/in_progress/completed counts.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-04")
    def test_summary_scoped_to_user(self, auth_client, db, test_user, test_admin):
        """
        TC-Summary-01 | Owner: Balaji | Requirement: TMA-F-033 | Backlog: S2-04
        Dashboard counts reflect only the current user's tasks.
        """
        pass

