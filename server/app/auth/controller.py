"""
Authentication controller — request/response parsing layer.
Owner: Balaji Gowda S R (PES2UG25CS804)
Sprint: S1 (S1-03)

TODO checklist:
  [ ] Parse and validate login request body
  [ ] Delegate to auth_service.authenticate()
  [ ] Build JSON response from User.to_dict()
  [ ] Handle AuthenticationError → 401
  [ ] Handle ValidationError → 400
"""


def handle_login(request_data: dict) -> dict:
    """
    TODO (S1-03 — Balaji): Parse login payload and call auth_service.
    Returns a dict to be serialized by the route.
    """
    raise NotImplementedError("handle_login not yet implemented (S1-03)")


def handle_logout() -> dict:
    """
    TODO (S1-03 — Balaji): Clear Flask-Login session.
    """
    raise NotImplementedError("handle_logout not yet implemented (S1-03)")

