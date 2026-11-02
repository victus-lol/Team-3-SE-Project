# Sprint 2 Regression Testing Checklist

**Backlog:** S2-10 — Security, Performance and Persistence Regression Testing  
**Issue:** [#24](https://github.com/victus-lol/Team-3-SE-Project/issues/24)  
**Owners:** Aadi Kore (QA/business-rule validation), Akash Pawar (persistence, performance setup, reporting/integration)  
**Last updated:** 2 November 2026  
**Status:** Baseline documented; several acceptance items remain blocked or not measured.

## 1. Purpose and status conventions

Use this checklist to record regression behavior after changes to authentication, authorization, tasks, notifications, persistence, and performance.

- **PASS:** The expected behavior was exercised and passed in the named test level.
- **PARTIAL:** Some checks passed, but a required path or security property is still pending.
- **BLOCKED:** The test cannot pass because the dependent API/feature is not implemented (for example, HTTP 501).
- **NOT RUN:** No execution evidence has been captured yet.
- **SKIPPED:** A test is present but deliberately skipped; it is not a pass.

Do not mark a feature complete because only its unauthenticated 401 guard or a frontend component with mocked API calls passes.

## 2. Current baseline

| Test level | Latest evidence | Current result |
|---|---|---|
| Backend unit + integration | Local Windows, Python 3.11.9, pytest 8.3.4 | 81 passed, 44 skipped, 0 failed |
| Backend statement coverage | Local `coverage.json` | 568 / 646 = 87.93% |
| Backend branch coverage | Local `coverage.json` | 66 / 92 = 71.74% |
| Frontend | GitHub Actions, Vitest 5.0.5 | 7 files / 15 tests passed; lint and build passed |
| Playwright E2E | Local Windows and GitHub Actions | 8 passed, 10 skipped, 0 failed |
| Full CI | Linux / Python 3.12 | All 5 jobs passed; backend 81 passed, 44 skipped; 88% line coverage |

Coverage percentages are reported separately by environment. CI currently measures line coverage and does not enable branch coverage; the 71.74% branch result is from the local Windows run.

## 3. Security and authentication regression checks

| Check | Procedure / test | Expected result | Latest observation | Status |
|---|---|---|---|---|
| Valid login | `TC-Auth-01`; auth API and Playwright valid login | Valid user gets a session and reaches protected workspace | Backend auth tests and Playwright scenario passed | **PASS** |
| Invalid login | `TC-Auth-02`; invalid password / unknown user | Generic authentication failure; no session | Backend auth tests and Playwright invalid-login scenario passed | **PASS** |
| Logout/session invalidation | `TC-Auth-03`; logout then call protected route | Session cleared; API access rejected and UI redirects to sign-in | Backend auth tests and Playwright login/logout passed | **PASS** |
| Unauthenticated API requests | `TC-Sec-01`; request protected task, notification, dashboard and admin routes without a session | HTTP 401 JSON response | Active API tests and Playwright anonymous API checks passed for the tested routes | **PASS (tested routes)** |
| Browser route protection | Open dashboard/tasks/admin routes while logged out | Redirect to sign-in | Playwright private-route redirect test passed | **PASS** |
| Standard user vs. admin | `TC-Sec-02`; standard user requests `GET /api/admin/users` | HTTP 403 | `test_admin_users_standard_user_returns_403` passed | **PASS (authorization gate)** |
| Admin user listing | Log in with admin test account and call `GET /api/admin/users` | Admin gets an authorized, safe user list | Route still returns HTTP 501 for admin caller | **BLOCKED** |
| Password hashing | `TC-Sec-03`; create user and verify stored password is a hash | Plaintext password is never stored | User model hashing tests passed | **PASS (hash storage)** |
| Password-hash API exclusion | `TC-Sec-03`; inspect all user-facing/admin API payloads | No `password_hash` field is exposed | Admin response test is skipped because listing endpoint is pending | **PARTIAL** |
| CSRF / cookie / transport settings | `TC-Sec-04`; verify CSRF behavior and production cookie/HTTPS settings in an explicitly configured environment | Unsafe requests are protected; production cookies/transport meet config policy | No dedicated executed check is recorded. E2E config inherits testing settings with CSRF disabled; E2E is not evidence of production CSRF behavior | **NOT RUN** |
| Hostile input | `TC-Sec-05`; submit hostile task fields and invalid search/sort input | Safe validation error; no crash, injection or internal trace | Hostile-input and invalid-sort tests are skipped; separate error-response test confirms stack traces are not returned | **PARTIAL** |

## 4. Core feature regression blockers

These are known implementation gaps, not failed CI tests. Anonymous requests may correctly return 401 while the authenticated feature endpoint remains unimplemented.

| Feature | Endpoints / modules to verify | Current observed behavior | Required next action | Status |
|---|---|---|---|---|
| Task create/list/retrieve | `GET/POST /api/tasks`, `GET /api/tasks/<id>` | Authenticated requests return HTTP 501; core integration cases are skipped | Implement service/routes, enable create/list/owner-scope tests and task CRUD E2E | **BLOCKED** |
| Task update/delete | `PATCH/DELETE /api/tasks/<id>` | Authenticated requests return HTTP 501; update/delete tests are skipped | Implement ownership-safe mutations and enable integration/E2E tests | **BLOCKED** |
| Task priority/status/date rules | `server/app/tasks/rules.py` | Rule functions raise `NotImplementedError`; 7 rule tests are skipped | Implement valid/invalid values, due-date parsing and state transitions | **BLOCKED** |
| Search/filter/sort | Task list query parameters and search service | Backend tests are skipped; UI controls have component tests but rely on local state/mocked data | Implement user-scoped query handling, allowlisted sorting and deterministic tie-break | **BLOCKED (backend); UI component checks pass** |
| Overdue detection | Task rules / overdue filter | Backend overdue rule is unimplemented and its tests are skipped | Implement timezone-aware overdue boundary behavior and filters | **BLOCKED** |
| Categories | `GET/POST /api/categories` | Authenticated endpoints return HTTP 501; create/list/scoping tests are skipped | Confirm category scope decision, then implement list/create/ownership tests | **BLOCKED / SCOPE DECISION** |
| Dashboard metrics | `GET /api/dashboard/summary` | Authenticated endpoint returns HTTP 501; summary tests are skipped | Implement current-user counts and enable integration tests | **BLOCKED** |
| Admin listing | `GET /api/admin/users` | Unauthenticated 401 and standard-user 403 pass; admin caller receives HTTP 501 | Implement authorized list and password-hash exclusion; enable admin E2E | **BLOCKED (admin action)** |
| Notification API | `GET /api/notifications`, `PATCH /api/notifications/<id>/read` | 15 unit/scheduler tests and 4 API integration tests pass | Preserve ownership checks; activate browser journeys when UI is integrated | **PASS (backend); E2E pending** |
| Notification UI error text | `client/src/features/notifications/NotificationPanel.jsx` | Error state still appends wording that says the notification API is awaiting implementation, although the API now exists | Remove/update stale fallback text and verify success, empty and error states | **FOLLOW-UP UI DEFECT** |

## 5. Persistence regression

**Not yet verified**

- [ ] Use a file-backed temporary SQLite database for this test; do not use the transient Playwright database.
- [ ] Create a record through the supported application/data layer and commit it.
- [ ] Close/remove the SQLAlchemy session and dispose the original engine/connection.
- [ ] Reopen the same database file using a new app context/connection (or controlled application restart).
- [ ] Retrieve the record and compare its identifier, owner and persisted fields.
- [ ] Verify foreign-key constraints remain enabled after reconnect.
- [ ] Clean up the temporary DB, WAL and SHM files after the test.

**Current evidence:** `server/tests/integration/test_persistence.py::test_task_persists_after_db_session_close` is skipped. The Playwright E2E runner deliberately creates and deletes a dedicated temporary SQLite database, so it does not satisfy application persistence acceptance.

**Acceptance evidence required:** A passing automated persistence test on a file-backed database and a recorded run result.

## 6. Performance regression

**Not measured**

The project test plan specifies 20 concurrent users over a 30-second window and p90 response time no greater than 3 seconds.

- [ ] Agree and record the test tool and environment (host OS, CPU/RAM, DB location, app server, network).
- [ ] Use a stable, seeded dataset and record dataset size.
- [ ] Exercise representative authenticated API operations once the task/dashboard endpoints are implemented.
- [ ] Run 20 virtual users for at least 30 seconds after warm-up.
- [ ] Capture request count, error rate, p50/p90/p95 latency and throughput.
- [ ] Confirm p90 ≤ 3 seconds, or record the failing endpoints and bottleneck evidence.
- [ ] Save the raw load-test output and summarize it in the validation report.

**Current evidence:** No load-test run or p90 measurement is recorded. Do not report the target as passed.

## 7. Frontend and browser regression

- [x] Authentication: valid login, invalid login and logout/protected-route checks (3 Playwright tests passed).
- [x] Platform smoke: health, readiness, sign-in screen, protected-route redirect and anonymous API access (5 Playwright tests passed).
- [x] Frontend CI: 7 Vitest files / 15 tests passed; lint and production build passed.
- [ ] Task CRUD browser journeys (3 tests currently skipped; backend APIs return 501).
- [ ] Search/filter/sort browser journeys (3 tests currently skipped; backend query behavior pending).
- [ ] Admin browser journeys (2 tests currently skipped; admin list route returns 501).
- [ ] Notification view/mark-as-read browser journeys (2 tests currently skipped; API passes unit/integration, browser integration pending).
- [ ] Responsive checks at agreed small/mobile, tablet and desktop viewport sizes.
- [ ] Keyboard-only navigation and visible focus validation.
- [ ] Accessible names/labels and color contrast review; record tool/manual evidence.

## 8. Re-run commands

From repository root, run each layer separately and retain output.

### Backend

```powershell
cd server
python -m pytest --cov=app --cov-branch --cov-report=term-missing --cov-report=json:coverage.json --junitxml=junit.xml
```

### Frontend

```powershell
cd ..\client
npm ci
npm run lint
npm test
npm run build
```

### Playwright E2E

Stop any manually started app servers first.

```powershell
cd ..\tests
npm ci
npx playwright install chromium
npm test
```

### Pending-test inventory

From repository root:

```powershell
python scripts/check_test_placeholders.py
```

Do not use `--fail-on-pending` as a release gate until the team agrees the remaining placeholders must all be completed; current skipped tests represent acknowledged feature work.

## 9. Ownership and handoff

| Owner | Regression follow-up |
|---|---|
| Aadi Kore | Task CRUD implementation/tests, task rules, overdue behavior, search/filter/sort, category scope and hostile-input validation |
| Balaji Gowda S R | Dashboard summary API, admin user listing, admin serialization and role checks |
| Akash Pawar | Persistence test setup, performance-test environment/reporting, regression evidence and CI integration |
| Aaryan Dubey | Connect task/search/dashboard/notification UI to completed APIs; fix stale notification error text; finish responsive/accessibility checks |

## 10. Exit criteria for S2-10

- [ ] Security regression cases TC-Sec-01 to TC-Sec-05 have actual outcomes recorded; pending transport/cookie and hostile-input cases are executed.
- [ ] File-backed persistence test passes after session close/reopen or controlled restart.
- [ ] Load test records 20 virtual users for 30 seconds and p90 ≤ 3 seconds, or a deviation is accepted and documented.
- [ ] Feature API blockers are resolved or formally moved to an agreed later sprint with owner and rationale.
- [ ] Applicable skipped tests are enabled; any remaining skipped test has an explicit deferral.
- [ ] Backend, frontend and E2E suites are rerun, with raw results attached or linked.
- [ ] Requirement matrix and system validation report are reviewed and updated.

**Current conclusion:** Authentication and notification backend regressions, health/readiness checks and available browser smoke tests pass. S2-10 is not complete: persistence and performance are unmeasured, multiple APIs return 501, and several security/feature tests remain skipped.
