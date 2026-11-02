# Unit Test Report

**Project:** Task Manager Application  
**Sprint:** Sprint 2 — notification implementation (S2-07)  
**Execution date:** 2 November 2026  
**Environment:** Windows, Python 3.11.9, pytest 8.3.4, pytest-cov 6.0.0  
**Branch:** `feature/s2-07-notifications`  
**Status:** Preliminary test execution report; testing remains in progress.

## 1. Test execution

Command used for the complete backend suite:

```powershell
python -m pytest --cov=app --cov-branch --cov-report=term-missing
```

Focused S2-07 test command:

```powershell
python -m pytest -v tests/unit/test_notification_service.py tests/integration/test_notifications_api.py
```

## 2. Results

| Test group | Passed | Skipped | Total |
|---|---:|---:|---:|
| Backend unit tests | 44 | 30 | 74 |
| Backend integration/API tests | 24 | 27 | 51 |
| **Backend total** | **68** | **57** | **125** |

Focused S2-07 result:

| Test file | Passed | Failed | Skipped |
|---|---:|---:|---:|
| `tests/unit/test_notification_service.py` | 15 | 0 | 0 |
| `tests/integration/test_notifications_api.py` | 4 | 0 | 0 |
| **Total** | **19** | **0** | **0** |

## 3. Unit-test file results

| Test file | Passed | Skipped |
|---|---:|---:|
| `tests/unit/test_auth_service.py` | 0 | 5 |
| `tests/unit/test_models.py` | 29 | 0 |
| `tests/unit/test_notification_service.py` | 15 | 0 |
| `tests/unit/test_search_service.py` | 0 | 7 |
| `tests/unit/test_task_rules.py` | 0 | 11 |
| `tests/unit/test_task_service.py` | 0 | 7 |
| **Total** | **44** | **30** |

## 4. S2-07 test coverage

The notification unit tests exercise:
- Notification creation and persistence.
- User-scoped notification listing.
- Read-state updates and ownership enforcement.
- Empty/oversized message validation.
- Linked-task ownership validation.
- Timezone-aware scheduled timestamps.
- Successful and unsuccessful provider delivery.
- Deferral of future notifications.
- Scheduler provider validation, start/stop behavior, queue processing and future reminders.

The notification integration tests exercise:
- Unauthenticated access rejection (401).
- Authenticated notification listing.
- User isolation in API responses.
- Marking an owned notification as read.
- Hiding another user's notification with a 404 response.

## 5. Skipped tests and limitations

The 57 skipped tests are existing pending tests for other incomplete project areas. They have not been counted as passed. They include authentication, task APIs/rules/services, search, persistence, categories, dashboard and admin scenarios.

The run completed with **68 passed, 57 skipped, 0 failed**. Six SQLAlchemy legacy API warnings were reported for existing `Query.get()` usage; these warnings did not fail the suite.

## 6. Conclusion

All 19 focused S2-07 notification tests passed locally. The full backend suite also completed without failures. The report is preliminary because the skipped test backlog and remaining system/E2E validation must be addressed during the scheduled testing window.
