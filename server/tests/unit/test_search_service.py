"""
Search service unit tests.
Owner: Aadi Kore (PES2UG24CS006)
"""

from datetime import date, timedelta

from app.search.service import search_tasks
from app.tasks.service import create_task


class TestSearchService:
    def test_keyword_search_matches_title(self, db, test_user):
        create_task(test_user.id, {"title": "Shopping list"})

        results = search_tasks(test_user.id, {"q": "Shopping"})

        assert len(results) == 1
        assert results[0].title == "Shopping list"

    def test_keyword_search_matches_description(self, db, test_user):
        create_task(
            test_user.id,
            {
                "title": "Task",
                "description": "Prepare presentation",
            },
        )

        results = search_tasks(
            test_user.id,
            {"q": "presentation"},
        )

        assert len(results) == 1

    def test_filter_by_status(self, db, test_user):
        create_task(test_user.id, {"title": "Pending"})
        create_task(
            test_user.id,
            {
                "title": "Completed",
                "status": "completed",
            },
        )

        results = search_tasks(
            test_user.id,
            {"status": "completed"},
        )

        assert len(results) == 1
        assert results[0].status == "completed"

    def test_filter_by_priority(self, db, test_user):
        create_task(
            test_user.id,
            {
                "title": "Urgent",
                "priority": "high",
            },
        )
        create_task(
            test_user.id,
            {
                "title": "Normal",
                "priority": "low",
            },
        )

        results = search_tasks(
            test_user.id,
            {"priority": "high"},
        )

        assert len(results) == 1
        assert results[0].title == "Urgent"

    def test_sort_by_due_date_deterministic(self, db, test_user):
        create_task(
            test_user.id,
            {
                "title": "Later",
                "due_date": (date.today() + timedelta(days=5)).isoformat(),
            },
        )
        create_task(
            test_user.id,
            {
                "title": "Earlier",
                "due_date": (date.today() + timedelta(days=1)).isoformat(),
            },
        )

        results = search_tasks(
            test_user.id,
            {"sort_by": "due_date", "order": "asc"},
        )

        assert results[0].title == "Earlier"

    def test_search_scoped_to_user(self, db, test_user, test_admin):
        create_task(test_user.id, {"title": "Private task"})
        create_task(test_admin.id, {"title": "Private task"})

        results = search_tasks(
            test_user.id,
            {"q": "Private"},
        )

        assert len(results) == 1
        assert results[0].owner_id == test_user.id

    def test_overdue_filter(self, db, test_user):
        create_task(
            test_user.id,
            {
                "title": "Overdue",
                "due_date": (date.today() - timedelta(days=2)).isoformat(),
            },
        )
        create_task(
            test_user.id,
            {
                "title": "Future",
                "due_date": (date.today() + timedelta(days=2)).isoformat(),
            },
        )

        results = search_tasks(
            test_user.id,
            {"overdue": "true"},
        )

        assert len(results) == 1
        assert results[0].title == "Overdue"
