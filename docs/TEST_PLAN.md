# Test Plan and Execution Record

**Reviewed:** 12 November 2026. The values below are measured local results unless marked GitHub Actions. Skipped tests are reported as skipped, never as passed.

## Test layers

| Layer | Tooling | Coverage |
|---|---|---|
| Static quality | Ruff, ESLint, placeholder inventory | Python syntax/name/style checks; JavaScript lint; pending-test markers |
| Backend | pytest and pytest-cov | service rules, Flask API behavior, database persistence, ownership, security and migrations |
| Frontend | Vitest and production build | React behavior, auth forms, account recovery, feature components and bundle compilation |
| Browser integration | Playwright Chromium | real Flask and Vite servers with a disposable SQLite database; authentication, task workflows, admin access, search, notifications, recovery request and responsive/accessibility checks |
| Security | pip-audit, npm audit, API regression tests | dependency vulnerabilities, authorization, request validation, password/session handling, headers and body limits |
| Performance | `tests/performance/tasks_load.py` | 20 authenticated virtual users reading paginated task lists for 30 seconds; p90 target <= 3,000 ms |
| Release | GitHub Actions packaging | compiled frontend and Flask app packaged with manifest and SHA-256 checksum; version tags publish a GitHub Release |

## Local execution commands

From `server/` in the project virtual environment:

```powershell
python -m pytest -q
python -m pytest --cov=app --cov-branch --cov-report=json:coverage.json --cov-report=term
ruff check app tests migrations
flask --app run.py db upgrade
```

From `client/`:

```powershell
npm test -- --run
npm run lint
npm run build
```

From `tests/`:

```powershell
npm test
```

The Playwright config starts isolated Flask and Vite servers. Its disposable test database is removed after the run.

## Performance run

Start the isolated test server from the repository root:

```powershell
server\venv\Scripts\python.exe tests\e2e\start_server.py
```

In another terminal, run:

```powershell
server\venv\Scripts\python.exe tests\performance\tasks_load.py --vus 20 --duration 30 --max-p90-ms 3000 --output performance-report.json
```

The script creates one cookie/CSRF-authenticated session per virtual user, exercises `GET /api/tasks?page=1&per_page=20`, reports p50/p90/max latency, request rate and errors, and exits nonzero on request failures or p90 above the threshold.

## Test-case map

| Test ID | Scenario | Main evidence |
|---|---|---|
| TC-Auth-01–03 | Valid/invalid login, logout, protected route behavior | `server/tests/integration/test_auth_api.py`, `tests/e2e/authentication.spec.js` |
| TC-Auth-04 | Registration, password reset privacy, single-use/expiry, session invalidation | `server/tests/integration/test_auth_api.py`, `client/src/tests/PasswordResetPage.test.jsx`, recovery E2E request |
| TC-Task-01–03 | Task create/list/update/delete, validation and owner isolation | `server/tests/integration/test_tasks_api.py`, task unit tests, `tests/e2e/task-crud.spec.js` |
| TC-Search-01–03 | Search, filters, overdue behavior and stable sorting | `server/tests/integration/test_search_api.py`, service tests, `tests/e2e/search-filter.spec.js` |
| TC-Category-01 | User-scoped category listing and creation | `server/tests/integration/test_categories_api.py` |
| TC-Summary-01 | User-scoped dashboard metrics | `server/tests/integration/test_summary_api.py`, dashboard service tests |
| TC-Notify-01 | Create/list/read, ownership, scheduler and provider outcomes | `server/tests/integration/test_notifications_api.py`, notification unit tests, Playwright read-state |
| TC-Admin-01 | Anonymous 401, standard user 403, admin listing/audit | `server/tests/integration/test_admin_api.py`, `tests/e2e/admin-access.spec.js` |
| TC-Sec-01–07 | CSRF/session behavior, password hashes, hostile input, login throttling, headers, request size and reset token secrecy | `server/tests/integration/test_security_api.py`, `test_auth_api.py` |
| TC-Data-01 | Data survives closing and reopening a database session | `server/tests/integration/test_persistence.py` |
| TC-Perf-01 | 20 VUs for 30 seconds; p90 <= 3 seconds | `tests/performance/tasks_load.py` |
| TC-UX-01 | Responsive layout, keyboard/focus behavior and accessibility scans | `tests/e2e/frontend-workflows.spec.js`, frontend component tests |

## Latest execution on 12 November 2026

| Check | Result |
|---|---:|
| Backend pytest | 167 passed, 0 skipped |
| Backend statement coverage | 84.69% |
| Backend branch coverage | 64.09% |
| Ruff | Passed |
| Frontend Vitest | 27 passed |
| ESLint | Passed |
| Vite production build | Passed |
| Playwright Chromium | 24 passed, 0 skipped |
| Performance | 3,786 requests, 0 failures, p50 157.33 ms, p90 172.89 ms, max 270.27 ms, 126.20 requests/s |
| Alembic migration upgrade | Passed through `2e1b7d5f930c` |

The performance result was measured against the local Windows development server and file-backed SQLite test database. It is evidence for that setup only, not a production capacity guarantee. GitHub Actions will run the load gate and publish its own job summary in the pipeline update.

## Known operational requirements

- Password reset delivery requires SMTP variables and the correct public frontend URL. Tests use a stub and do not send real email.
- The notification scheduler remains manually driven and uses its test-provider abstraction; a production worker and provider are not claimed.
- GitHub Release packaging is configured. No hosting provider or live deployment credentials are configured.
