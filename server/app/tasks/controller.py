"""
Task controller — request/response parsing.
Owner: Aadi Kore (PES2UG24CS006)
Sprint: S1 (S1-04, S1-05)

TODO checklist:
  [ ] Parse and validate create/update payloads using schemas.py
  [ ] Call task_service functions
  [ ] Map service exceptions to HTTP responses
"""


def handle_create_task(owner_id: int, data: dict) -> dict:
    """TODO (S1-04 — Aadi): Parse create payload, call service."""
    raise NotImplementedError("handle_create_task not implemented (S1-04)")


def handle_update_task(task_id: int, owner_id: int, data: dict) -> dict:
    """TODO (S1-04 — Aadi): Parse update payload, call service."""
    raise NotImplementedError("handle_update_task not implemented (S1-04)")

