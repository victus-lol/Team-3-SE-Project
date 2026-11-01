"""
Categories API integration tests.
Owner: Aadi Kore (PES2UG24CS006)
Sprint: S2 (S2-01)
Requirement IDs: TMA-F-030, TMA-F-031
"""

import pytest


class TestCategoriesApiLive:
    def test_list_categories_unauthenticated_returns_401(self, client):
        """
        TC-Sec-01 | Owner: Aadi | Requirement: TMA-SR-001 | Backlog: S2-01
        GET /api/categories without auth returns 401.
        """
        response = client.get("/api/categories")
        assert response.status_code == 401


class TestCategoriesApi:
    @pytest.mark.skip(reason="Pending implementation: S2-01")
    def test_list_categories_authenticated(self, auth_client, sample_category):
        """
        TC-Org-04 | Owner: Aadi | Requirement: TMA-F-030 | Backlog: S2-01
        GET /api/categories returns user's categories.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-01")
    def test_category_not_visible_to_other_user(self, auth_client, db, test_admin):
        """
        TC-Org-04 | Owner: Aadi | Requirement: TMA-F-030 | Backlog: S2-01
        Categories are scoped to the owning user.
        """
        pass

