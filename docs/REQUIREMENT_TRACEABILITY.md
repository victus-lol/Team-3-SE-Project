# Requirement Traceability Matrix

**Project:** Team 3 Task Manager
**Reviewed:** 12 November 2026
**Source of truth:** `docs/SPRINT_PLAN.md`, current Flask/React source, pytest/Vitest/Playwright results, and the latest GitHub Actions runs.

Status reflects executable evidence. A closed backlog issue alone is not a test result. Historical snapshot sections from earlier drafts were removed because they described routes and tests that have since changed.

| Requirement | Current implementation | Verification evidence | Status / limitation |
|---|---|---|---|
| TMA-F-001, TMA-F-002 Authentication and sessions | Registration, login/logout, safe current-user profile, CSRF, persistent login throttling, password reset and session-version invalidation | `server/tests/integration/test_auth_api.py`; auth service tests; Playwright auth and recovery request workflows | PASS; SMTP delivery requires deployment configuration |
| TMA-F-010–012 Task CRUD | Authenticated task create/read/update/delete, ownership checks, business validation | task API/service tests; Playwright task lifecycle | PASS |
| TMA-F-020, TMA-F-030 Task rules and categories | Priority/status/date validation, category ownership and create/list APIs | task rules, task API, category API tests | PASS |
| TMA-F-021–023 Search, filters, overdue and sorting | User-scoped keyword search, multi-field filters, overdue filter, allowlisted stable sorting | search service/API tests; Playwright search/filter/sort | PASS |
| TMA-F-033 Dashboard summary | Current user's task metrics | dashboard API/service tests; Playwright dashboard | PASS |
| TMA-F-040–042 Notifications | User-scoped list/read, provider abstraction and manually driven scheduler | notification unit/API tests; Playwright list/read workflow | PASS for implemented test-provider/manual scheduler scope; no production worker/provider is claimed |
| TMA-SR-001 Role authorization | Admin-only user and audit endpoints; task/category/notification ownership | admin, task, category and notification integration tests; Playwright admin access | PASS |
| TMA-SR-003 Password and secret handling | Werkzeug hashes, safe serializers, hashed reset tokens, audit records omit credentials, prior sessions revoked on reset | model/auth/security/admin tests | PASS |
| TMA-SR-005 Input/security hardening | Request validation, CSRF, rate limiting, security headers, 1 MiB default request cap, generic errors | security/auth integration tests and security audit workflow | PASS; headers are configured for API responses; HTTPS HSTS is sent only on secure requests |
| TMA-NF-001 Persistence | SQLite-backed application, migration chain, data survives closing and reopening an independent database session | `server/tests/integration/test_persistence.py` | PASS for session close/reopen; whole-process restart was not benchmarked separately |
| TMA-NF-002 Performance | 20 concurrent authenticated virtual users request paginated task lists for 30 seconds | `tests/performance/tasks_load.py`; Windows local SQLite run on 12 Nov 2026: 3,786 requests, 0 failures, p50 157.33 ms, p90 172.89 ms, max 270.27 ms, 126.2 requests/s | PASS in the recorded local environment; performance varies by machine and database |
| TMA-NF-005 Responsive and accessible UI | Responsive pages, keyboard handling, focus management, skip link, contrast improvements | Playwright/Axe viewport checks at 375, 768, and 1440 px; Vitest component suite | PASS for the documented pages and checks |
| API contract and test traceability | REST reference and OpenAPI specification updated to current routes; test IDs mapped in this matrix and `docs/TEST_PLAN.md` | Review against Flask route registration and test modules; Prettier YAML syntax check locally and in Stage 1 | PASS; CI formatting/syntax gate is configured in PR #52 |

## Current local execution snapshot

| Suite | Result |
|---|---:|
| Backend pytest | 167 passed, 0 skipped |
| Backend statement coverage | 84.69% (1,084 / 1,280 statements) |
| Backend branch coverage | 64.09% (191 / 298 branches) |
| Backend Ruff | Passed |
| Frontend Vitest | 27 passed |
| Frontend ESLint | Passed |
| Frontend production build | Passed |
| Playwright Chromium | 24 passed, 0 skipped |
| Performance benchmark | 20 VUs / 30 s, 3,786 requests, p90 172.89 ms, 0 failures |
| Database upgrade | Passed through the current password-reset migration |

The checks are measured independently; coverage percentages are reported by the coverage quality gate rather than inferred from test counts.
