# Regression Validation Checklist

**Last verified:** 12 November 2026
**Evidence:** local backend/frontend/Playwright runs, local performance benchmark, and GitHub Actions runs for PRs #47–#50.

## Code quality and tests

- [x] Ruff backend lint
- [x] ESLint frontend lint
- [x] Backend unit and integration suite: 167 passed, 0 skipped
- [x] Frontend Vitest suite: 27 passed
- [x] Frontend production build
- [x] Playwright Chromium suite: 24 passed, 0 skipped
- [x] Placeholder inventory: zero pending markers
- [x] Python and Node dependency audits on GitHub Actions
- [x] Alembic migration upgrade on local development database

## Functional and security paths

- [x] Registration, login/logout, CSRF flow and safe profile serialization
- [x] Password reset privacy response, token hash-at-rest, expiry, one-time use, session revocation
- [x] Task CRUD, user ownership, validation, filtering, overdue behavior and stable sorting
- [x] Category create/list user scope; dashboard metrics
- [x] Notification list/read and role/owner authorization
- [x] Admin users/audit endpoints and secret-free audit record
- [x] Login throttling, security headers, oversized-body response, hostile-input regression
- [x] File-backed persistence after database session close/reopen

## Performance and measured coverage

- [x] 20 authenticated virtual users for 30 seconds against task listing
- [x] 3,786 requests, 0 failures, p90 172.89 ms, below the 3,000 ms target in the local Windows/SQLite environment
- [x] Line coverage 84.69%; branch coverage 64.09%; combined coverage 80.80%

## Deployment and operational limitations

- [ ] SMTP credentials and public frontend URL must be supplied by the deployment operator before password reset email delivery works.
- [ ] A production notification worker/provider remains a separate deployment decision.
- [ ] No hosting provider is configured; GitHub Actions builds a release artifact and does not deploy a live site.

Performance and coverage are machine/environment-sensitive. The CI pipeline publishes its own result; the local values above do not guarantee production capacity.
