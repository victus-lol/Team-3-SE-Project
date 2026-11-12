"""Admin user-management query service."""

from ..models.user import User


def list_users(page: int = 1, per_page: int = 20) -> list:
    """Return a stable page of users without exposing authentication secrets."""
    return User.query.order_by(User.id.asc()).paginate(
        page=max(1, page), per_page=min(max(1, per_page), 100), error_out=False
    ).items
