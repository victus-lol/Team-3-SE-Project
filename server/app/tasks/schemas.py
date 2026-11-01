"""
Task validation schemas.
Owner: Aadi Kore (PES2UG24CS006)
Sprint: S1 (S1-04), S2 (S2-01)
Requirement IDs: TMA-F-010, TMA-F-020

TODO checklist:
  [ ] Define CREATE_TASK_SCHEMA with required/optional fields and constraints
  [ ] Define UPDATE_TASK_SCHEMA (all fields optional, at least one required)
  [ ] Implement validate(data, schema) → (cleaned_data, errors)
  [ ] Validate field types, lengths, enum values (delegate to rules.py)
"""

# Schema constants (to be implemented in S1-04)
CREATE_TASK_SCHEMA = {
    "title": {"required": True, "type": str, "max_length": 200},
    "description": {"required": False, "type": str, "max_length": 2000},
    "priority": {"required": False, "type": str, "choices": ["low", "medium", "high"]},
    "status": {"required": False, "type": str, "choices": ["pending", "in_progress", "completed"]},
    "due_date": {"required": False, "type": str, "format": "YYYY-MM-DD"},
    "category_id": {"required": False, "type": int, "nullable": True},
}

UPDATE_TASK_SCHEMA = {
    "title": {"required": False, "type": str, "max_length": 200},
    "description": {"required": False, "type": str, "max_length": 2000},
    "priority": {"required": False, "type": str, "choices": ["low", "medium", "high"]},
    "status": {"required": False, "type": str, "choices": ["pending", "in_progress", "completed"]},
    "due_date": {"required": False, "type": str, "format": "YYYY-MM-DD"},
    "category_id": {"required": False, "type": int, "nullable": True},
}


def validate_create_task(data: dict) -> tuple[dict, list]:
    """
    TODO (S1-04 — Aadi): Validate data against CREATE_TASK_SCHEMA.
    Returns (cleaned_data, errors). errors is [] on success.
    """
    raise NotImplementedError("validate_create_task not implemented (S1-04)")


def validate_update_task(data: dict) -> tuple[dict, list]:
    """
    TODO (S1-04 — Aadi): Validate data against UPDATE_TASK_SCHEMA.
    Returns (cleaned_data, errors).
    """
    raise NotImplementedError("validate_update_task not implemented (S1-04)")

