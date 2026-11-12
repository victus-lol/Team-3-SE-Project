# API Documentation

The complete OpenAPI 3.0 specification is available at [docs/openapi.yaml](openapi.yaml).

## Base URL
`/api`

## Response Envelopes

### Success
```json
{
  "success": true,
  "data": {},
  "message": "Operation successful"
}
```

## Authentication and CSRF

Authentication uses the Flask session cookie. Sign-in, account creation, password-reset, and recovery routes are public; task, category, dashboard, notification, profile, and admin routes require a session. Admin routes require the `admin` role. Obtain a CSRF token from `GET /api/auth/csrf` before sending `POST`, `PATCH`, or `DELETE` requests, and send it in the `X-CSRFToken` header. Browser clients include cookies and this header automatically.

## Endpoint reference

| Method and path | Access | Purpose and key input |
|---|---|---|
| `GET /api/health`, `GET /api/ready` | Public | Liveness and database readiness checks. |
| `GET /api/auth/csrf` | Public | Start/refresh the CSRF token. |
| `POST /api/auth/register` | Public | `name`, `email`, `password`; always creates a standard user. Returns 201; duplicate email returns 409. |
| `POST /api/auth/login` | Public | `email`, `password`; returns a session, 401 for invalid credentials, or 429 during a configured lockout. |
| `POST /api/auth/logout` | Public | Clears the current session. |
| `GET /api/auth/me` | Session | Return the current user's safe profile. |
| `PATCH /api/auth/me` | Session | Update `name` only; attempts to update role, email, status, or other protected fields return 400. |
| `POST /api/auth/password-reset/request` | Public | Accepts `email`; always returns the same 202 message. A link is sent only when the email exists and SMTP is configured. |
| `POST /api/auth/password-reset/confirm` | Public | Accepts `token` and `password`; valid single-use links update the password and invalidate existing sessions. |
| `GET /api/tasks` | Session | List own tasks. Supports `q`, `status`, `priority`, `category_id`, `due_date_from`, `due_date_to`, `overdue`, `sort_by`, `order`, `page`, and `per_page`. |
| `POST /api/tasks` | Session | Create an owned task with title, description, priority, status, due date, and optional category ID. |
| `GET /api/tasks/{taskId}` | Session | Retrieve an owned task; foreign or missing IDs return 404. |
| `PATCH /api/tasks/{taskId}` | Session | Update an owned task using the same editable fields and business rules. |
| `DELETE /api/tasks/{taskId}` | Session | Delete an owned task. |
| `GET /api/categories`, `POST /api/categories` | Session | List own categories or create one with a `name`. |
| `GET /api/dashboard/summary` | Session | Return the authenticated user's task counts. |
| `GET /api/notifications` | Session | List only the authenticated user's notifications. |
| `PATCH /api/notifications/{notificationId}/read` | Session | Mark an owned notification read; foreign IDs return 404. |
| `GET /api/admin/users` | Admin | List safe user records; accessing this endpoint is audit logged. |
| `GET /api/admin/audit-logs` | Admin | Read the paginated, secret-free administrator audit history. |

## Request fields and constraints

| Operation | JSON fields / query parameters | Validation and defaults |
|---|---|---|
| Registration | `name`, `email`, `password` | Name 1–128 chars; valid email up to 254 chars; password 8–128 chars. A supplied role is never used to grant administrator access. |
| Login | `email`, `password` | Invalid credentials return the same 401 response; configured lockout returns 429. |
| Profile update | `name` | Required, 1–128 chars. Only `name` can be changed. |
| Password reset | request: `email`; confirm: `token`, `password` | Reset password 8–128 chars; invalid, expired, or reused token returns 400. Request always returns 202 to avoid account enumeration. |
| Task create/update | `title`, `description`, `priority`, `status`, `due_date`, `category_id` | Title 1–200 chars; description up to 2,000 chars or null; priority `low\|medium\|high`; status `pending\|in_progress\|completed`; due date ISO `YYYY-MM-DD`; category ID positive integer or null. Create requires title; update requires at least one editable field. Unknown fields are rejected. |
| Task list | `q`, `status`, `priority`, `category_id`, `due_date_from`, `due_date_to`, `overdue`, `sort_by`, `order`, `page`, `per_page` | `page` defaults to 1; `per_page` defaults to 20 and is capped at 100; invalid values return 400. Sort fields are allow-listed in the OpenAPI spec. |
| Category create | `name` | Trimmed name 1–100 chars; normalized lowercase; duplicate name for the same user returns 409. |
| Audit log list | `page`, `per_page` | `page` defaults to 1; `per_page` defaults to 50 and is capped at 100. Admin role required. |

## Representative API examples

Create a task after obtaining a CSRF token and signing in:

```http
POST /api/tasks
Content-Type: application/json
X-CSRFToken: <csrf-token>
```

```json
{
  "title": "Review sprint deliverables",
  "description": "Check the release checklist",
  "priority": "high",
  "status": "pending",
  "due_date": "2026-11-20",
  "category_id": null
}
```

Successful create returns HTTP 201 with the task object in `data`; invalid input returns HTTP 400, a missing session returns HTTP 401, and a category not owned by the caller is rejected. A missing or non-owned task returns HTTP 404 without disclosing whether another user's task exists.

### Task list pagination

`page` defaults to 1 and `per_page` defaults to 20. Both must be positive integers; `per_page` is capped at 100. Filtering and deterministic sorting are applied before pagination. The existing `data` array remains unchanged and pagination metadata is a sibling field:

```json
{
  "success": true,
  "data": [],
  "message": "Operation successful",
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total_items": 0,
    "total_pages": 0,
    "has_next": false,
    "has_previous": false
  }
}
```

## Error status codes

Validation errors return 400; unauthenticated and unauthorized requests return 401 and 403; missing or non-owned resources return 404; duplicate registrations/categories return 409; oversized bodies return 413; login lockouts return 429. Error responses use the standard `success: false` envelope and do not include stack traces or credential material.

### Error
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input provided"
  }
}
```

