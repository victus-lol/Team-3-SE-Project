"""
Search service unit tests.
Owner: Aadi Kore (PES2UG24CS006)
Sprint: S2 (S2-02)
Requirement IDs: TMA-F-021, TMA-F-022, TMA-F-023
"""

import pytest


class TestSearchService:
    @pytest.mark.skip(reason="Pending implementation: S2-02")
    def test_keyword_search_matches_title(self, db, test_user, sample_task):
        """
        TC-Search-01 | Owner: Aadi | Requirement: TMA-F-021 | Backlog: S2-02
        Keyword in title returns matching task.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-02")
    def test_keyword_search_matches_description(self, db, test_user, sample_task):
        """
        TC-Search-01 | Owner: Aadi | Requirement: TMA-F-021 | Backlog: S2-02
        Keyword in description returns matching task.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-02")
    def test_filter_by_status(self, db, test_user):
        """
        TC-Search-02 | Owner: Aadi | Requirement: TMA-F-021 | Backlog: S2-02
        Filter by status returns only matching tasks.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-02")
    def test_filter_by_priority(self, db, test_user):
        """
        TC-Search-02 | Owner: Aadi | Requirement: TMA-F-021 | Backlog: S2-02
        Filter by priority returns only matching tasks.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-02")
    def test_sort_by_due_date_deterministic(self, db, test_user):
        """
        TC-Search-03 | Owner: Aadi | Requirement: TMA-F-023 | Backlog: S2-02
        Sorting by due_date is deterministic (secondary sort by id).
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-02")
    def test_search_scoped_to_user(self, db, test_user, test_admin):
        """
        TC-Sec-01 | Owner: Aadi | Requirement: TMA-F-021 | Backlog: S2-02
        Search results never include another user's tasks.
        """
        pass

    @pytest.mark.skip(reason="Pending implementation: S2-02")
    def test_overdue_filter(self, db, test_user):
        """
        TC-Monitor-01 | Owner: Aadi | Requirement: TMA-F-022 | Backlog: S2-02
        overdue=true filter returns only overdue tasks.
        """
        pass

