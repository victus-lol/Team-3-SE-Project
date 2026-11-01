"""
Category service.
Owner: Aadi Kore (PES2UG24CS006)
Sprint: S2 (S2-01)
Requirement IDs: TMA-F-030, TMA-F-031

TODO checklist:
  [ ] Implement list_categories(user_id) → list[Category]
  [ ] Implement create_category(user_id, name) → Category
  [ ] Enforce unique name per user (case-insensitive via normalization)
  [ ] Prevent cross-user category access
"""

from ..models.category import Category


def list_categories(user_id: int) -> list:
    """TODO (S2-01 — Aadi): List all categories owned by user_id."""
    raise NotImplementedError("list_categories not implemented (S2-01)")


def create_category(user_id: int, name: str) -> Category:
    """
    TODO (S2-01 — Aadi): Create a category for user_id.
    Raise ConflictError if normalized name already exists for this user.
    """
    raise NotImplementedError("create_category not implemented (S2-01)")


def get_category_or_404(category_id: int, user_id: int) -> Category:
    """
    TODO (S2-01 — Aadi): Get category, raise NotFoundError if not owned by user.
    Called by task service to validate category ownership before assigning.
    """
    raise NotImplementedError("get_category_or_404 not implemented (S2-01)")

