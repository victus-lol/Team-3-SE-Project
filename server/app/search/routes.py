"""
Search routes.
Owner: Aadi Kore (PES2UG24CS006)
Sprint: S2 (S2-02)
Requirement IDs: TMA-F-021, TMA-F-022, TMA-F-023

Note: Search is served via GET /api/tasks with query parameters.
This blueprint handles /api/tasks search params forwarding if needed
as a separate concern. See tasks/routes.py for the primary endpoint.

TODO checklist:
  [ ] Implement keyword search across title and description (user-scoped)
  [ ] Implement filters: status, priority, category_id, due_date_from, due_date_to, overdue
  [ ] Implement sorting: allowlisted fields, deterministic secondary sort by task ID
  [ ] Never interpolate raw column names — use allowlist mapping
  [ ] Write integration tests in tests/integration/test_search_api.py
"""

from flask import Blueprint

search_bp = Blueprint("search", __name__)

# Note: primary search endpoint is GET /api/tasks (handled by tasks_bp)
# This blueprint is reserved for any additional search-specific routes if needed.
