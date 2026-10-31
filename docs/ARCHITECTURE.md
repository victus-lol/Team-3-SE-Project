# Architecture Overview

## Layered Backend Architecture
```
HTTP Requests -> Routes -> Controllers -> Services -> Models (SQLAlchemy ORM) -> SQLite DB
```
1. **Routes (`app/<module>/routes.py`):** Blueprint endpoint declarations, HTTP verb routing, status codes, and JSON serialization.
2. **Controllers (`app/<module>/controller.py`):** Parses parameters, validates payload formats, invokes services.
3. **Services (`app/<module>/service.py`):** Business logic, authorization rules, transaction orchestration.
4. **Models (`app/models/*.py`):** Data entities, DB constraints, relationships, serialization helpers.

## Security Architecture
- Password Hashing: Werkzeug PBKDF2/SHA256. Plaintext passwords never stored or logged.
- CSRF Protection: Flask-WTF CSRF enabled on state-changing methods. Frontend passes `X-CSRFToken` header.
- Sessions: Flask-Login with secure HTTP-only and SameSite cookies.
- Authorization: Route decorators enforce authentication and role access server-side.

