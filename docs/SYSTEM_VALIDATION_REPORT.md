# System Validation Report

**Project:** Task Manager Application  
**Sprint:** Sprint 2 — current validation snapshot  
**Execution date:** 2 November 2026  
**Environment:** Windows, Python 3.11.9, Flask test client, pytest 8.3.4  
**Branch:** `feature/s2-07-notifications`  
**Status:** Preliminary / partial validation — not final system sign-off.

## 1. Objective

Record the backend API/integration validation executed against the current Sprint 2 feature branch and identify scenarios that remain pending before final system acceptance.

## 2. Execution

Command:

```powershell
python -m pytest --cov=app --cov-branch --cov-report=term-missing
```

Focused notification API execution:

```powershell
python -m pytest -v tests/unit/test_notification_service.py tests/integration/test_notifications_api.py
```

## 3. Backend integration test results

| Integration test file | Passed | Skipped | Validation area |
|---|---:|---:|---|
| `test_admin_api.py` | 2 | 2 | Admin access |
| `test_auth_api.py` | 0 | 8 | Login/session |
| `test_categories_api.py` | 1 | 2 | Category API |
| `test_health_api.py` | 11 | 0 | Health, readiness and database checks |
| `test_notifications_api.py` | 4 | 0 | Notification API and ownership |
| `test_persistence.py` | 0 | 1 | Persistence |
| `test_search_api.py` | 0 | 4 | Search and sorting |
| `test_security_api.py` | 2 | 3 | Authentication/access and error response checks |
| `test_summary_api.py` | 1 | 2 | Dashboard summary |
| `test_tasks_api.py` | 3 | 5 | Task API |
| **Total** | **24** | **27** | |

## 4. S2-07 notification validation

| Scenario | Expected result | Observed result |
|---|---|---|
| GET notifications without login | 401 | Passed |
| GET notifications with login | 200 and standard response envelope | Passed |
| User has own and foreign notifications | Only own records returned | Passed |
| Mark own notification as read | Status becomes `read` | Passed |
| Mark another user's notification as read | 404 without exposing foreign record | Passed |

The related unit-level service and scheduler tests also passed (15/15).

## 5. Overall backend test status

| Result | Count |
|---|---:|
| Passed | 68 |
| Skipped / pending | 57 |
| Failed | 0 |
| **Total collected** | **125** |

## 6. Outstanding validation

This execution does **not** constitute complete end-to-end system validation. The following areas still have skipped/pending tests:
- Login, logout and session behavior.
- Task CRUD and task authorization cases.
- Search, filters and deterministic sorting.
- Persistence across session/application restart.
- Some category, dashboard and admin cases.
- Full browser-based Playwright workflows.
- Frontend-to-backend integration against a running application.

The frontend CI checks passed on the pull request, but that does not replace full Playwright E2E or integrated system validation.

## 7. Conclusion

The current backend snapshot has no failing tests, and the S2-07 notification service/API cases pass. Final system validation remains **in progress** until the pending cases are implemented or formally deferred, E2E workflows are executed, and the complete Test Plan is reviewed. No final acceptance claim is made by this preliminary report.
