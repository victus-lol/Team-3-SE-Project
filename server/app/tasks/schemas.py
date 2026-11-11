"""
Task validation schemas.
Owner: Aadi Kore (PES2UG24CS006)
Sprint: S1 (S1-04), S2 (S2-01)
"""

from datetime import datetime

from ..common.exceptions import ValidationError
from .rules import validate_due_date, validate_priority, validate_status

CREATE_TASK_SCHEMA = {
    "title": {"required": True},
    "description": {"required": False},
    "priority": {"required": False},
    "status": {"required": False},
    "due_date": {"required": False},
    "category_id": {"required": False},
}

UPDATE_TASK_SCHEMA = {
    "title": {"required": False},
    "description": {"required": False},
    "priority": {"required": False},
    "status": {"required": False},
    "due_date": {"required": False},
    "category_id": {"required": False},
}

ALLOWED_FIELDS = set(CREATE_TASK_SCHEMA)


def _validate(data: dict, *, creating: bool) -> tuple[dict, list]:
    if not isinstance(data, dict):
        return {}, ["Request body must be a JSON object."]

    errors = []
    cleaned = {}

    unknown = set(data) - ALLOWED_FIELDS
    if unknown:
        errors.append(f"Unknown fields: {', '.join(sorted(unknown))}")

    if creating and "title" not in data:
        errors.append("Title is required.")

    if not creating and not data:
        errors.append("At least one field must be provided.")

    for field in ALLOWED_FIELDS:
        if field not in data:
            continue

        value = data[field]

        if field == "title":
            if not isinstance(value, str):
                errors.append("Title must be a string.")
                continue
            value = value.strip()
            if not value:
                errors.append("Title cannot be empty.")
            elif len(value) > 200:
                errors.append("Title cannot exceed 200 characters.")
            else:
                cleaned[field] = value

        elif field == "description":
            if value is None:
                cleaned[field] = None
            elif not isinstance(value, str):
                errors.append("Description must be a string or null.")
            elif len(value) > 2000:
                errors.append("Description cannot exceed 2000 characters.")
            else:
                cleaned[field] = value

        elif field == "priority":
            try:
                validate_priority(value)
                cleaned[field] = value
            except ValidationError as exc:
                errors.append(str(exc))

        elif field == "status":
            try:
                validate_status(value)
                cleaned[field] = value
            except ValidationError as exc:
                errors.append(str(exc))

        elif field == "due_date":
            try:
                parsed = validate_due_date(value)
                cleaned[field] = parsed
            except ValidationError as exc:
                errors.append(str(exc))

        elif field == "category_id":
            if value is None:
                cleaned[field] = None
            elif isinstance(value, bool) or not isinstance(value, int):
                errors.append("Category ID must be an integer or null.")
            elif value <= 0:
                errors.append("Category ID must be positive.")
            else:
                cleaned[field] = value

    return cleaned, errors


def validate_create_task(data: dict) -> tuple[dict, list]:
    """Validate and normalize a task creation payload."""
    return _validate(data, creating=True)


def validate_update_task(data: dict) -> tuple[dict, list]:
    """Validate and normalize a task update payload."""
    return _validate(data, creating=False)