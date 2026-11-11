"""
Task controller.
Owner: Aadi Kore (PES2UG24CS006)
"""

from ..common.exceptions import ValidationError
from .schemas import validate_create_task, validate_update_task
from .service import create_task, update_task


def handle_create_task(owner_id: int, data: dict) -> dict:
    cleaned, errors = validate_create_task(data)

    if errors:
        raise ValidationError(
            "Task validation failed.",
            {"errors": errors},
        )

    task = create_task(owner_id, cleaned)
    return task.to_dict()


def handle_update_task(task_id: int, owner_id: int, data: dict) -> dict:
    cleaned, errors = validate_update_task(data)

    if errors:
        raise ValidationError(
            "Task validation failed.",
            {"errors": errors},
        )

    task = update_task(task_id, owner_id, cleaned)
    return task.to_dict()