# Backend Unit and Integration Test Report

**Project:** Team 3 Task Manager
**Execution date:** 12 November 2026
**Environment:** Windows, Python 3.12.6, pytest in `server/venv`
**Current branch:** `codex/qa-docs-performance`

## Latest full run

Command from `server/`:

```powershell
python -m pytest -q
```

| Result | Count |
|---|---:|
| Passed | 167 |
| Skipped | 0 |
| Failed | 0 |
| SQLAlchemy deprecation warnings | 2 |

The suite covers auth and registration, password reset token privacy/expiry/reuse/session invalidation, user profile protection, task CRUD/ownership/rules, categories, search and pagination, dashboard summaries, notifications, admin authorization/audit, HTTP hardening, and persistence after closing/reopening a file-backed database session.

Frontend and browser results are recorded separately in `docs/TEST_PLAN.md`; they are not included in the backend count.

## Coverage

The same backend suite was run with pytest-cov branch measurement. See `docs/CODE_COVERAGE_REPORT.md` and `docs/BRANCH_COVERAGE_REPORT.md` for separate line and branch calculations.

## Warnings

Two existing model tests use the legacy SQLAlchemy `Query.get()` API. The warning is non-failing; replacing it is cleanup work and does not affect this test result.
