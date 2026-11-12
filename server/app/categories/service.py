"""
Category service.
Owner: Aadi Kore (PES2UG24CS006)
Sprint: S2 (S2-01)
"""

from sqlalchemy.exc import IntegrityError

from ..common.exceptions import ConflictError, NotFoundError, ValidationError
from ..extensions import db
from ..models.category import Category


def list_categories(user_id: int) -> list:
    """Return only categories belonging to the specified user."""
    return (
        Category.query.filter_by(user_id=user_id)
        .order_by(Category.name.asc(), Category.id.asc())
        .all()
    )


def create_category(user_id: int, name: str) -> Category:
    """Create a normalized category for one user."""
    if not isinstance(name, str) or not name.strip() or len(name.strip()) > 100:
        raise ValidationError("Category name must contain 1 to 100 characters.")
    category = Category.create(user_id, name)
    db.session.add(category)
    try:
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise ConflictError("A category with this name already exists.") from exc
    return category


def get_category_or_404(category_id: int, user_id: int) -> Category:
    """Return an owned category or raise NotFoundError."""
    category = Category.query.filter_by(
        id=category_id,
        user_id=user_id,
    ).first()

    if category is None:
        raise NotFoundError("Category not found.")

    return category
