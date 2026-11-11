"""
Search service.
Owner: Aadi Kore (PES2UG24CS006)
Sprint: S2 (S2-02)
"""

from datetime import date

from sqlalchemy import asc, desc, or_

from ..common.exceptions import ValidationError
from ..models.task import Task
from ..tasks.rules import (
    SORTABLE_FIELDS,
    validate_due_date,
    validate_priority,
    validate_status,
)


def search_tasks(user_id: int, params: dict | None = None) -> list:
    params = params or {}

    query = Task.query.filter(Task.owner_id == user_id)

    keyword = params.get("q", "").strip()

    if keyword:
        pattern = f"%{keyword}%"
        query = query.filter(
            or_(
                Task.title.ilike(pattern),
                Task.description.ilike(pattern),
            )
        )

    status = params.get("status")
    if status:
        validate_status(status)
        query = query.filter(Task.status == status)

    priority = params.get("priority")
    if priority:
        validate_priority(priority)
        query = query.filter(Task.priority == priority)

    category_id = params.get("category_id")
    if category_id not in (None, ""):
        try:
            category_id = int(category_id)
        except (TypeError, ValueError) as exc:
            raise ValidationError(
                "Category ID must be an integer."
            ) from exc

        if category_id <= 0:
            raise ValidationError("Category ID must be positive.")

        query = query.filter(Task.category_id == category_id)

    date_from = params.get("due_date_from")
    if date_from:
        query = query.filter(
            Task.due_date >= validate_due_date(date_from)
        )

    date_to = params.get("due_date_to")
    if date_to:
        query = query.filter(
            Task.due_date <= validate_due_date(date_to)
        )

    overdue = params.get("overdue")

    if overdue not in (None, ""):
        if overdue not in ("true", "false"):
            raise ValidationError(
                "Overdue must be true or false."
            )

        if overdue == "true":
            query = query.filter(
                Task.due_date.isnot(None),
                Task.due_date < date.today(),
                Task.status != "completed",
            )
        else:
            query = query.filter(
                (Task.due_date.is_(None))
                | (Task.due_date >= date.today())
                | (Task.status == "completed")
            )

    sort_by = params.get("sort_by", "created_at")
    order = params.get("order", "desc")

    if sort_by not in SORTABLE_FIELDS:
        raise ValidationError("Invalid sort field.")

    if order not in ("asc", "desc"):
        raise ValidationError("Invalid sort order.")

    columns = {
        "created_at": Task.created_at,
        "updated_at": Task.updated_at,
        "due_date": Task.due_date,
        "priority": Task.priority,
        "status": Task.status,
        "title": Task.title,
    }

    column = columns[sort_by]

    query = query.order_by(
        asc(column) if order == "asc" else desc(column),
        asc(Task.id),
    )

    return query.all()