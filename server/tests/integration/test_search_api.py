"""
Search API integration tests.
Owner: Aadi Kore (PES2UG24CS006)
Sprint: S2 (S2-02)
Requirement IDs: TMA-F-021, TMA-F-022, TMA-F-023
"""

import pytest


class TestSearchApi:
    @pytest.mark.skip(reason="Pending implementation: S2-02")
    def test_search_by_keyword(self, auth_client, sample_task):
        """
        TC-Search-01 | Owner: Aadi | Requirement: TMA-F-021 | Backlog: S2-02
        GET /api/tasks?q=keyword returns matching tasks.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-02")
    def test_filter_by_status(self, auth_client):
        """
        TC-Search-02 | Owner: Aadi | Requirement: TMA-F-021 | Backlog: S2-02
        GET /api/tasks?status=pending returns only pending tasks.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-02")
    def test_sort_by_created_at(self, auth_client):
        """
        TC-Search-03 | Owner: Aadi | Requirement: TMA-F-023 | Backlog: S2-02
        GET /api/tasks?sort_by=created_at returns deterministically sorted tasks.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-02")
    def test_invalid_sort_field_rejected(self, auth_client):
        """
        TC-Sec-05 | Owner: Aadi | Requirement: TMA-SR-003 | Backlog: S2-02
        GET /api/tasks?sort_by=injected_column returns 400 (allowlist enforced).
        """
        pass

