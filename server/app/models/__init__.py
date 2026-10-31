"""
Models package — import all models here so SQLAlchemy / Alembic sees them.
Every model must be imported in this file before migrations are generated.
"""

from .category import Category
from .notification import Notification
from .task import Task
from .user import User

__all__ = ["User", "Task", "Category", "Notification"]

