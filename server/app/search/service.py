"""
Search service — keyword search, filtering, sorting for tasks.
Owner: Aadi Kore (PES2UG24CS006)
Sprint: S2 (S2-02)
Requirement IDs: TMA-F-021, TMA-F-022, TMA-F-023

TODO checklist:
  [ ] Implement search_tasks(user_id, params) → list[Task]
  [ ] Keyword: LIKE %q% on title and description (case-insensitive in SQLite)
  [ ] Filter: status, priority, category_id, due_date_from, due_date_to, overdue
  [ ] Sort: allowlisted fields only; secondary sort by id for determinism
  [ ] Write unit tests in tests/unit/test_search_service.py (TC-Search-01..03)
"""



def search_tasks(user_id: int, params: dict) -> list:
    """
    TODO (S2-02 — Aadi): Apply all search/filter/sort params and return matching tasks.
    All results MUST be scoped to user_id.
    TC-Search-01, TC-Search-02, TC-Search-03 | Requirement: TMA-F-021 | Backlog: S2-02
    """
    raise NotImplementedError("search_tasks not implemented (S2-02)")

