# Requirement Traceability Matrix (RTM)

**Project:** Team 3 Task Manager  
**Last reviewed:** 2 November 2026  
**Baseline:** `main` after S2-09 / PR #38 merge  
**Status convention:** `PASS` = implemented and exercised by the stated test level; `PARTIAL` = some layers or paths pass but required functionality/verification remains; `PENDING` = not implemented, skipped, or not measured. A passing authorization guard for an unimplemented endpoint does not mean the endpoint's business feature is complete.

| Req ID | Requirement | Owner | Backend / Frontend implementation | Test cases and evidence | Current status |
|---|---|---|---|---|---|
| TMA-F-001 | User login and authentication | Balaji / Aaryan | `server/app/auth/`; `client/src/features/auth/` | `TC-Auth-01`; `test_auth_service.py` (5 passed); `test_auth_api.py` (8 passed); Playwright valid/invalid login; LoginPage Vitest | **PASS** — login and invalid-credential behavior verified at API and browser level |
| TMA-F-002 | User logout and session invalidation | Balaji / Aaryan | Auth controller/routes; AuthContext / Navbar | `TC-Auth-03`; auth API logout/session tests; Playwright login/logout | **PASS** — logout and protected-route behavior verified |
| TMA-F-010 | Task creation and retrieval | Aadi / Aaryan | Task routes currently return 501; task UI and API client exist | `TC-Task-01`; authenticated create/list tests skipped; task routes return 501; UI tests use mocked API | **PENDING** — real task list/create/retrieval is not implemented |
| TMA-F-011 | Task update | Aadi / Aaryan | PATCH task route returns 501; TaskForm UI exists | `TC-Task-02`; authenticated update test skipped; TaskForm component test uses mocked API | **PENDING** — real update endpoint is not implemented |
| TMA-F-012 | Task deletion | Aadi / Aaryan | DELETE task route returns 501; TaskList confirmation UI exists | `TC-Task-03`; authenticated delete test skipped; TaskList component test uses mocked API | **PENDING** — real delete endpoint is not implemented |
| TMA-F-020 | Priority, status and due-date rules | Aadi | `server/app/tasks/rules.py` has unimplemented rule functions; task UI fields exist | `TC-Org-01`, `TC-Org-02`, `TC-Org-03`; 7 task-rule unit tests skipped | **PENDING** — rule functions currently raise NotImplementedError |
| TMA-F-021 | Task search and multi-field filtering | Aadi / Aaryan | Search/filter UI exists; backend task/search routes do not implement query behavior | `TC-Search-01`, `TC-Search-02`; 7 search service tests and 4 search API tests skipped; TaskFilters UI tests pass with local state | **PARTIAL** — UI controls exist and are unit-tested; backend search/filter is pending |
| TMA-F-022 | Overdue task detection | Aadi | UI computes an overdue filter locally; backend `is_overdue` is unimplemented | `TC-Monitor-01`; overdue unit tests skipped | **PENDING** — backend overdue rule/filter is not implemented or verified |
| TMA-F-023 | Deterministic task sorting | Aadi | Search blueprint is a placeholder; task list endpoint returns 501 | `TC-Search-03`; sorting API and unit tests skipped | **PENDING** — deterministic server-side sorting is not implemented |
| TMA-F-030 | Category association and user scoping | Aadi | Category model exists; category list route returns 501; task create flow is unimplemented | `TC-Org-04`; authenticated category/listing tests skipped; unauthenticated guard test returns 401 | **PARTIAL** — model baseline exists, but category API and association flow are pending |
| TMA-F-031 | Category creation | Aadi | POST `/api/categories` returns 501; scope decision remains pending | Category creation acceptance/test case not active; category API file documents scope-pending | **PENDING / SCOPE DECISION** — endpoint is not implemented |
| TMA-F-033 | Dashboard task metrics | Balaji / Aaryan | Dashboard UI exists; GET `/api/dashboard/summary` returns 501 | `TC-Summary-01`; 2 authenticated summary tests skipped; Dashboard Vitest tests use mocked APIs | **PARTIAL** — UI behavior is component-tested; live summary API is pending |
| TMA-F-040 | Notification generation and user-scoped listing | Akash / Aaryan | Notification model/service/routes; NotificationPanel UI | `TC-Notify-01`; 15 notification service/scheduler unit tests and 4 notification API integration tests passed; NotificationPanel Vitest tests passed; E2E notification journey skipped | **PASS (backend) / PARTIAL (browser integration)** — create/list behavior is verified; full browser journey remains deferred |
| TMA-F-041 | Notification read-state updates | Akash / Aaryan | `mark_notification_read` service and PATCH route; NotificationPanel UI | `TC-Notify-01`; unit/API ownership and read tests passed; component test passed; Playwright mark-as-read journey skipped | **PASS (backend/component) / PARTIAL (E2E)** — API and component behavior verified; browser workflow pending |
| TMA-F-042 | Notification provider abstraction and scheduler | Akash | Provider interface, dispatch service and manually driven scheduler | `TC-Notify-01`; provider success/failure, future scheduling, queue start/stop tests included in 15 passing unit tests | **PASS (test-provider scope)** — injectable provider and scheduler behavior verified; production provider/worker is not claimed |
| TMA-SR-001 | Role-based authorization | Balaji / Akash | `login_required_json`, `admin_required`; ProtectedRoute; task owner checks cannot be exercised because task routes are stubs | `TC-Sec-01`, `TC-Sec-02`; admin API unauthenticated 401 and standard-user 403 pass; anonymous API and protected-route E2E checks pass | **PARTIAL** — authentication/role gates are verified; admin listing and task-owner operations remain pending |
| TMA-SR-003 | Secure password hashing and secret handling | Balaji | User model hashes passwords and serializes a limited public representation; admin API is not implemented | Model tests (29 passed, including password hashing); `TC-Sec-03` admin response exclusion test skipped; transport/cookie checks not evidenced | **PARTIAL** — password hashing is verified; API-wide secret exclusion and transport/cookie verification remain |
| TMA-SR-005 | Input sanitization and validation | Aadi / Balaji | Task/category APIs and task validation paths are incomplete | `TC-Sec-05`; hostile-input test skipped; invalid sort-field test skipped; generic error response does not expose stack traces | **PENDING** — hostile-input validation is not yet verified |
| TMA-NF-001 | Persistence across application restart | Akash / Aadi | SQLite configuration exists; test E2E database is disposable by design | `TC-Data-01`; `test_persistence.py` skipped | **NOT VERIFIED** — no successful restart-persistence test is recorded |
| TMA-NF-002 | Response time p90 ≤ 3 seconds under agreed load | Akash / Aadi | Whole API / UI | `TC-Perf-01`; no measured 20-user load-test result is recorded | **NOT MEASURED** — performance acceptance remains open |
| TMA-NF-005 | Responsive UI and accessibility | Aaryan | Responsive app shell and feature components exist | `TC-UX-01`; frontend CI: 7 Vitest files / 15 tests passed; no dedicated automated accessibility report is recorded | **PARTIAL** — component suite passes; explicit responsive and accessibility acceptance checks remain |

## Latest execution snapshot

Execution evidence is split by environment and test level; the figures below are not combined into one coverage percentage.

| Test level | Environment / source | Result |
|---|---|---|
| Backend unit + integration | Local Windows, Python 3.11.9, pytest 8.3.4 | 81 passed, 44 skipped, 0 failed (125 collected) |
| Backend statement coverage | Local Windows, pytest-cov 6.0.0 | 568 / 646 statements = 87.93% (approximately 88%) |
| Backend branch coverage | Local Windows, pytest-cov 6.0.0 | 66 / 92 branches = 71.74% |
| Frontend component tests | GitHub Actions, Vitest 5.0.5 | 7 files, 15 tests passed |
| Playwright E2E | Local Windows and GitHub Actions | 8 passed, 10 skipped, 0 failed |
| Full GitHub Actions workflow | Linux / Python 3.12 | 5 / 5 jobs passed; backend 81 passed, 44 skipped; 88% line coverage |

## Deferred / known gaps

- Task routes (`GET/POST /api/tasks`, `GET/PATCH/DELETE /api/tasks/<id>`) currently return HTTP 501 after authentication; task CRUD is not complete.
- Task rules, overdue detection, server-side search/filtering/sorting, category APIs, dashboard summary and admin user listing remain incomplete or scope-pending.
- Persistence-after-restart and performance-load acceptance have not been demonstrated.
- Playwright task CRUD, search/filter, admin and notification-interaction journeys remain skipped. Skipped tests are not passing evidence.
- The E2E database is intentionally temporary and must not be used as evidence of application persistence.
- CI and local coverage values are reported separately because the CI job measures line coverage on Linux/Python 3.12, while the local branch metric was measured on Windows/Python 3.11.9.

**Interpretation:** Authentication and notification service/API capabilities have executable verification. Several UI components are covered with mocked API responses, but that does not prove end-to-end integration with the unfinished backend endpoints. This matrix is a current implementation/test snapshot, not final system acceptance.
