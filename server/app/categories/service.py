"""
Category service.
Owner: Aadi Kore (PES2UG24CS006)
Sprint: S2 (S2-01)
"""

from ..common.exceptions import NotFoundError
from ..models.category import Category


def list_categories(user_id: int) -> list:
    """Return only categories belonging to the specified user."""
    return (
        Category.query.filter_by(user_id=user_id)
        .order_by(Category.name.asc(), Category.id.asc())
        .all()
    )


def create_category(user_id: int, name: str) -> Category:
    """Category creation is pending scope approval."""
    raise NotImplementedError("Category creation is pending scope approval.")


def get_category_or_404(category_id: int, user_id: int) -> Category:
    """Return an owned category or raise NotFoundError."""
    category = Category.query.filter_by(
        id=category_id,
        user_id=user_id,
    ).first()

    if category is None:
        raise NotFoundError("Category not found.")

    return category
