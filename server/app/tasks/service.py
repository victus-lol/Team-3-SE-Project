"""
Task service: database operations and ownership enforcement.
Owner: Aadi Kore (PES2UG24CS006)
"""

from sqlalchemy import asc, desc

from ..categories.service import get_category_or_404
from ..common.exceptions import NotFoundError, ValidationError
from ..extensions import db
from ..models.task import Task
from .rules import (
    allowed_status_transitions,
    validate_due_date,
    validate_priority,
    validate_status,
)


def get_task_or_404(task_id: int, user_id: int) -> Task:
    task = Task.query.filter_by(id=task_id, owner_id=user_id).first()
    if task is None:
        raise NotFoundError("Task not found.")
    return task


def list_tasks(user_id: int, filters: dict | None = None) -> list:
    query = Task.query.filter_by(owner_id=user_id)
    filters = filters or {}

    if filters.get("status"):
        validate_status(filters["status"])
        query = query.filter(Task.status == filters["status"])

    if filters.get("priority"):
        validate_priority(filters["priority"])
        query = query.filter(Task.priority == filters["priority"])

    if filters.get("category_id") not in (None, ""):
        try:
            category_id = int(filters["category_id"])
        except (TypeError, ValueError):
            raise ValidationError("Category ID must be an integer.")
        query = query.filter(Task.category_id == category_id)

    sort_by = filters.get("sort_by", "created_at")
    order = filters.get("order", "desc")

    allowed = {
        "created_at": Task.created_at,
        "updated_at": Task.updated_at,
        "due_date": Task.due_date,
        "priority": Task.priority,
        "status": Task.status,
        "title": Task.title,
    }

    if sort_by not in allowed:
        raise ValidationError("Invalid sort field.")
    if order not in {"asc", "desc"}:
        raise ValidationError("Sort order must be asc or desc.")

    sort_column = allowed[sort_by]
    query = query.order_by(
        (asc(sort_column) if order == "asc" else desc(sort_column)),
        asc(Task.id),
    )
    return query.all()


def create_task(owner_id: int, data: dict) -> Task:
    if not isinstance(data, dict) or not data.get("title"):
        raise ValidationError("A valid task title is required.")

    values = dict(data)

    if "priority" in values:
        validate_priority(values["priority"])
    if "status" in values:
        validate_status(values["status"])
    if "due_date" in values:
        values["due_date"] = validate_due_date(values["due_date"])

    category_id = values.get("category_id")
    if category_id is not None:
        get_category_or_404(category_id, owner_id)

    task = Task(owner_id=owner_id, **values)
    db.session.add(task)
    db.session.commit()
    return task


def update_task(task_id: int, user_id: int, data: dict) -> Task:
    task = get_task_or_404(task_id, user_id)

    if not isinstance(data, dict) or not data:
        raise ValidationError("At least one field must be provided.")

    values = dict(data)

    if "priority" in values:
        validate_priority(values["priority"])
    if "status" in values:
        validate_status(values["status"])
        if not allowed_status_transitions(task.status, values["status"]):
            raise ValidationError("This status transition is not allowed.")
    if "due_date" in values:
        values["due_date"] = validate_due_date(values["due_date"])

    if values.get("category_id") is not None:
        get_category_or_404(values["category_id"], user_id)

    for field, value in values.items():
        setattr(task, field, value)

    db.session.commit()
    return task


def delete_task(task_id: int, user_id: int) -> None:
    task = get_task_or_404(task_id, user_id)
    db.session.delete(task)
    db.session.commit()
