# End-to-end tests

The Playwright suite lives in this directory and starts the Flask API and Vite
frontend automatically. It uses the Flask `testing` configuration, which keeps
the E2E database isolated from the developer database.

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
starts the API on port 5000 and the client on port 5173.

## Current coverage boundary

The active smoke tests verify API health/readiness, the public sign-in screen,
logged-out redirects, and anonymous access controls for task, notification,
and admin endpoints.

The authentication, task CRUD, search/filter, admin-user listing, and
notification read/write user journeys remain skipped placeholders while their
dependent feature APIs/UI are unfinished. A skipped test is not a passing
feature test. Add executable scenarios when the owning feature is implemented
and available for integration testing.
