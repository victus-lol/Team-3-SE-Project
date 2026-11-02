# End-to-end tests

The Playwright suite starts an isolated Flask API and the Vite frontend.
The E2E server creates a temporary SQLite database per run and seeds dedicated
test-only user accounts. It does not use the developer's normal database.

## Local setup (Windows PowerShell)

From the repository root:

```powershell
cd tests
npm install
npx playwright install chromium
npm test
```

To run with a visible browser:

```powershell
npm run test:headed
```

To open the HTML report after a run:

```powershell
npm run report
```

Stop any manually started app servers before running the suite. Playwright
starts its own API server on port 5000 and Vite client on port 5173. The E2E
API server removes its temporary database when it exits.

## Seeded E2E accounts

These credentials exist only in the isolated E2E database:

| Role | Email | Password |
|---|---|---|
| Standard user | `e2e.user@example.com` | `password123` |
| Admin | `e2e.admin@example.com` | `adminpassword123` |

Do not reuse these credentials outside automated tests.

## Current coverage boundary

Active browser tests cover:
- API health and database readiness.
- Public sign-in form rendering.
- Valid login and logout.
- Invalid login rejection.
- Redirects from protected routes when logged out.
- Anonymous API access controls for task, notification, and admin endpoints.

Task CRUD, search/filter, admin-user listing, and notification interaction journeys
remain skipped placeholders until the dependent features are ready for full
integration testing. A skipped test is not counted as passing feature coverage.
