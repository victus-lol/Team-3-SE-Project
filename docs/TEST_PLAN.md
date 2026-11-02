# Test Plan and Execution Record

## 1. Test strategy

- **Unit tests:** Validate individual service methods, rules, models, and UI components in isolation.
- **Integration tests:** Verify HTTP request/response lifecycles, database behavior and authorization decorators.
- **E2E tests:** Use Playwright against managed Flask and Vite servers with a dedicated disposable SQLite database.
- **CI:** Run backend lint/tests, frontend lint/tests/build, placeholder inventory and Playwright E2E on pushes and pull requests to `main`.

## 2. Test case catalogue and latest execution

Status meanings:
- **PASS:** Expected behavior was observed in the recorded test.
- **SKIPPED / PENDING:** The test exists but its implementation or prerequisites are incomplete. It is not a pass.
- **NOT RUN:** No execution evidence is available for the scenario.

| Test ID | Scenario / expected result | Actual result in latest evidence | Status |
|---|---|---|---|
| TC-Auth-01 | Valid credentials establish an authenticated session | Auth service/API tests and Playwright valid login passed | **PASS** |
| TC-Auth-02 | Invalid credentials are rejected without authenticating the user | Auth API and Playwright invalid-credentials tests passed | **PASS** |
| TC-Auth-03 | Logout invalidates the session; subsequent protected access is rejected | Auth API logout/session tests and Playwright login/logout flow passed | **PASS** |
| TC-Task-01 | Authenticated user can create and list/retrieve only their own tasks | Core authenticated task tests skipped; authenticated task routes return HTTP 501 | **SKIPPED / BLOCKED** |
| TC-Task-02 | User can update an owned task; another user's task is not exposed | Core update tests skipped; PATCH task route returns HTTP 501 | **SKIPPED / BLOCKED** |
| TC-Task-03 | User can delete an owned task after confirmation | Backend delete test and Playwright task-delete flow skipped; DELETE route returns HTTP 501 | **SKIPPED / BLOCKED** |
| TC-Org-01 | Valid priority values are accepted and invalid values rejected | Task-rule unit tests skipped; rule function is not implemented | **SKIPPED / PENDING** |
| TC-Org-02 | Valid due date is parsed; invalid date is rejected | Due-date unit tests skipped; rule function is not implemented | **SKIPPED / PENDING** |
| TC-Org-03 | Valid status values/transitions are accepted; invalid transitions rejected | Status-rule unit tests skipped; rule function is not implemented | **SKIPPED / PENDING** |
| TC-Org-04 | Category list/association is scoped to the authenticated owner | Authenticated category API tests skipped; category routes return HTTP 501 | **SKIPPED / PENDING** |
| TC-Search-01 | Keyword search matches task title/description for the current user | Search unit/API and Playwright keyword-search tests skipped; task API query implementation pending | **SKIPPED / PENDING** |
| TC-Search-02 | Multi-field filters return only matching tasks | Backend search/filter tests skipped; frontend filter-control component tests passed with local state/mocks | **PARTIAL** |
| TC-Search-03 | Sorting returns deterministic order for the requested allowlisted field | Backend sorting and Playwright sorting tests skipped | **SKIPPED / PENDING** |
| TC-Monitor-01 | Past-due incomplete tasks are overdue; today's/completed/no-date tasks are not | Overdue rule tests skipped; backend rule is not implemented | **SKIPPED / PENDING** |
| TC-Notify-01 | Notification creation, user-scoped listing, read-state, validation, scheduling and provider outcomes behave as specified | 15 service/scheduler unit tests and 4 notification API integration tests passed; NotificationPanel component tests passed; Playwright notification journeys remain skipped | **PASS (unit/API/component); E2E PENDING** |
| TC-Summary-01 | Dashboard summary returns current user's pending/in-progress/completed counts | Two authenticated summary tests skipped; summary endpoint returns HTTP 501; dashboard component tests use mocked APIs | **SKIPPED / BLOCKED** |
| TC-Admin-01 | Unauthenticated request returns 401; standard user returns 403; admin can list users safely | 401 and 403 integration checks passed; admin list and password-hash exclusion tests skipped; admin listing route returns HTTP 501 for admin caller | **PARTIAL** |
| TC-Perf-01 | p90 response time is ≤ 3 seconds under 20 concurrent users over the agreed window | No load-test execution result recorded | **NOT RUN** |
| TC-Rel-01 | Health/readiness endpoints confirm service/database availability | Health API suite (11 tests) passed; Playwright health and readiness smoke tests passed | **PASS (smoke scope)** |
| TC-Data-01 | Created data remains retrievable after closing/reopening DB session or restarting the app | Persistence integration test is skipped; E2E database is intentionally deleted after each run | **SKIPPED / NOT VERIFIED** |
| TC-UX-01 | Main UI is responsive and meets agreed accessibility checks | Frontend CI passed 7 Vitest files / 15 tests; no dedicated accessibility audit/result recorded | **PARTIAL** |
| TC-Sec-01 | Protected API endpoints reject unauthenticated access with 401; browser routes redirect to sign-in | Task/admin/notification/other protected API auth checks and Playwright anonymous-access/redirect checks passed | **PASS (tested endpoints)** |
| TC-Sec-02 | Standard user is rejected from admin endpoint with 403 | `test_admin_users_standard_user_returns_403` passed | **PASS** |
| TC-Sec-03 | Password hashes are not exposed by API responses | User password hashing/model tests passed; admin API serialization test skipped because listing endpoint is pending | **PARTIAL** |
| TC-Sec-04 | Transport and cookie protections meet project security settings | No dedicated executed test result is recorded | **NOT RUN** |
| TC-Sec-05 | Hostile input is safely rejected; error responses do not disclose internal traces | Stack-trace disclosure test passed; hostile-input and invalid-sort tests remain skipped | **PARTIAL** |

## 3. Detailed notification test cases (S2-07)

| Test ID | Scenario | Expected result | Actual result | Status |
|---|---|---|---|---|
| TC-Notify-01a | Create a notification for an existing user | Persisted with pending status and UTC timestamp policy | Unit test passed | PASS |
| TC-Notify-01b | List notifications when own and foreign records exist | Only the authenticated user's records are returned | Unit and API user-scope tests passed | PASS |
| TC-Notify-01c | Mark an owned notification as read | Status becomes `read`; repeated request remains safe | Unit and API tests passed | PASS |
| TC-Notify-01d | Mark another user's notification as read | 404 without exposing the foreign record | Unit and API tests passed | PASS |
| TC-Notify-01e | Submit empty or oversized message | Validation error; no record created | Unit validation test passed | PASS |
| TC-Notify-01f | Reference another user's task | Ownership check rejects the reference | Unit test passed | PASS |
| TC-Notify-01g | Dispatch before `scheduled_at` | Remains pending; provider not called | Unit test passed | PASS |
| TC-Notify-01h | Provider reports successful delivery | Status becomes delivered with delivery timestamp | Unit test passed | PASS |
| TC-Notify-01i | Provider reports failure | Status becomes failed; delivery timestamp remains empty | Unit test passed | PASS |
| TC-Notify-01j | Scheduler stopped/not started | Queued notifications are not dispatched | Unit test passed | PASS |
| TC-Notify-01k | Scheduler starts and due queue is processed | Provider called and processed item leaves queue | Unit test passed | PASS |

## 4. Latest execution summary

### Local backend (Windows / Python 3.11.9)

Command:

```powershell
cd server
python -m pytest --cov=app --cov-branch --cov-report=term-missing --cov-report=json:coverage.json --junitxml=junit.xml
```

| Metric | Result |
|---|---:|
| Collected | 125 |
| Passed | 81 |
| Skipped | 44 |
| Failed | 0 |
| Statement coverage | 568 / 646 = 87.93% (approximately 88%) |
| Branch coverage | 66 / 92 = 71.74% |

Nine SQLAlchemy `LegacyAPIWarning` warnings were emitted; they did not cause test failures.

### Frontend (GitHub Actions / Vitest 5.0.5)

- 7 test files passed.
- 15 tests passed.
- Frontend lint and production build passed.

### Playwright E2E (local Windows and GitHub Actions)

| E2E scenario group | Passed | Skipped |
|---|---:|---:|
| Authentication (login/logout, invalid credentials, protected redirect) | 3 | 0 |
| Platform smoke/security checks (health, readiness, sign-in, protected routes, anonymous API) | 5 | 0 |
| Task CRUD | 0 | 3 |
| Search/filter/sort | 0 | 3 |
| Admin access | 0 | 2 |
| Notification interaction | 0 | 2 |
| **Total** | **8** | **10** |

The full CI workflow completed with all five jobs passing. CI backend tests on Linux/Python 3.12 also reported 81 passed and 44 skipped, with 88% line coverage. CI does not currently enable branch coverage; the 71.74% branch figure is from the local Windows run.

## 5. Known limitations and deferred work

1. Authenticated task endpoints currently return HTTP 501; task CRUD acceptance remains open.
2. Task validation rules, overdue detection, server-side search/filter/sorting, category APIs, dashboard summary and admin user listing remain incomplete or scope-pending.
3. Persistence-after-restart has not been tested successfully; the Playwright database is deliberately ephemeral.
4. Performance target p90 ≤ 3 seconds at 20 concurrent users has not been measured.
5. Explicit accessibility/responsiveness checks and transport/cookie security checks need a documented execution result.
6. Playwright task CRUD, search/filter, admin and notification interaction scenarios remain skipped. Do not count skipped cases as passed.
7. The notification scheduler is intentionally manually driven until the team agrees on production scheduling/worker policy; no production provider or worker is claimed.

## 6. Exit criteria for final validation

- Resolve or formally defer all skipped tests with owner and rationale.
- Implement remaining API routes and enable their authenticated integration/E2E tests.
- Complete persistence and performance measurements in a reproducible environment.
- Record responsive/accessibility and transport/cookie verification.
- Re-run the full backend, frontend and Playwright suites and update this execution record.
- Review the completed requirement matrix with the feature owners before declaring final acceptance.

**Current conclusion:** Authentication and notification backend scenarios are verified, and available platform smoke/security checks pass. Overall project system validation remains in progress because several feature APIs and acceptance tests are still pending.
