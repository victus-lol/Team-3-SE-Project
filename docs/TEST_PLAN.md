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
| TC-Task-01 | Authenticated user can create and list/retrieve only their own tasks | New live Playwright workflow created and listed a task through the current API | **PASS (E2E)** |
| TC-Task-02 | User can update an owned task; another user's task is not exposed | New live Playwright workflow updated its owned task; cross-user API case is outside this UI check | **PASS (E2E owned task)** |
| TC-Task-03 | User can delete an owned task after confirmation | New live Playwright workflow cancelled and confirmed deletion through the current API | **PASS (E2E)** |
| TC-Org-01 | Valid priority values are accepted and invalid values rejected | Backend task-rule unit tests passed | **PASS (unit)** |
| TC-Org-02 | Valid due date is parsed; invalid date is rejected | Backend task-rule unit tests passed | **PASS (unit)** |
| TC-Org-03 | Valid status values/transitions are accepted; invalid transitions rejected | Backend task-rule unit tests passed | **PASS (unit)** |
| TC-Org-04 | Category list/association is scoped to the authenticated owner | Backend category API tests passed, including visibility scope | **PASS (API)** |
| TC-Search-01 | Keyword search matches task title/description for the current user | Backend search API and live Playwright workflow both verified keyword search | **PASS (API/E2E)** |
| TC-Search-02 | Multi-field filters return only matching tasks | Live Playwright sent status, priority, and overdue filters together and confirmed the matching overdue task remained visible; component tests cover filter controls and reset | **PASS (component/E2E)** |
| TC-Search-03 | Sorting returns deterministic order for the requested allowlisted field | Backend API accepts the allowlisted created-at sort and rejects an invalid field; the API test checks the response but not the actual ordering; UI sorting remains a skipped legacy scenario | **PARTIAL** |
| TC-Monitor-01 | Past-due incomplete tasks are overdue; today's/completed/no-date tasks are not | Backend task-rule unit tests passed for due today, past due, completed, and no due date | **PASS (unit)** |
| TC-Notify-01 | Notification creation, user-scoped listing, read-state, validation, scheduling and provider outcomes behave as specified | 15 service/scheduler unit tests and 4 notification API integration tests passed; NotificationPanel tests and new live mark-read Playwright workflow passed | **PASS (unit/API/component/E2E)** |
| TC-Summary-01 | Dashboard summary returns current user's pending/in-progress/completed counts | Backend summary API tests passed for counts, empty state, and user scope; live Playwright confirmed dashboard data loads | **PASS (API/E2E)** |
| TC-Admin-01 | Unauthenticated request returns 401; standard user returns 403; admin can list users safely | 401 and 403 integration checks passed; admin list and password-hash exclusion tests skipped; admin listing route returns HTTP 501 for admin caller | **PARTIAL** |
| TC-Perf-01 | p90 response time is ≤ 3 seconds under 20 concurrent users over the agreed window | No load-test execution result recorded | **NOT RUN** |
| TC-Rel-01 | Health/readiness endpoints confirm service/database availability | Health API suite (11 tests) passed; Playwright health and readiness smoke tests passed | **PASS (smoke scope)** |
| TC-Data-01 | Created data remains retrievable after closing/reopening DB session or restarting the app | Persistence integration test is skipped; E2E database is intentionally deleted after each run | **SKIPPED / NOT VERIFIED** |
| TC-UX-01 | Main UI is responsive and meets agreed accessibility checks | New Playwright checks verified no horizontal overflow and Axe WCAG 2.1 AA scans on login, dashboard, tasks, and notifications at 375px, 768px, and 1440px; keyboard skip link and modal focus/Escape/restore were checked | **PASS (scoped frontend checks)** |
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

### Previous coverage run (Windows / Python 3.11.9; 2 November 2026)

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

### Local backend rerun (Windows / Python 3.12; 12 November 2026)

Command: `python -m pytest -q` from `server/` after installing `tzdata` in the local virtual environment. The initial run had two due-date tests fail because this Windows environment lacked zoneinfo data; after the local-only install the result was **137 passed, 5 skipped, 0 failed**. No backend source or dependency manifest was changed for this environment fix. The skips are tracked in the pending-test inventory.

### Frontend (local / Vitest 5.0.5)

- 8 test files passed.
- 22 tests passed.
- Frontend lint and production build passed.

### Playwright E2E (local Windows and GitHub Actions)

Latest local run on 12 November 2026 used the current Flask API and disposable E2E database. It completed **13 passed, 10 skipped, 0 failed**. The five new frontend workflows covered task CRUD/search/filter, live dashboard data, notification read-state, keyboard/mobile behavior, and Axe accessibility scans at three viewport widths. The ten existing skipped tests remain skipped; they include admin, reminders, sorting, and older task CRUD placeholders. The new task CRUD checks are separate live coverage and passed.

| E2E scenario group | Passed | Skipped |
|---|---:|---:|
| Authentication (login/logout, invalid credentials, protected redirect) | 3 | 0 |
| Platform smoke/security checks (health, readiness, sign-in, protected routes, anonymous API) | 5 | 0 |
| New frontend workflows (task CRUD/search/filter, dashboard, notification, keyboard/mobile, accessibility) | 5 | 0 |
| Legacy task CRUD placeholders | 0 | 3 |
| Legacy search/filter/sort placeholders | 0 | 3 |
| Admin access | 0 | 2 |
| Notification interaction placeholders | 0 | 2 |
| **Total** | **13** | **10** |

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

**Current conclusion:** The assigned frontend work is implemented and passes local unit, lint, build, live API workflow, responsive, keyboard, and accessibility checks. Overall project validation remains in progress because shared E2E placeholders (including admin, reminders, and sorting) and broader performance/persistence/security criteria remain open for their owners.
