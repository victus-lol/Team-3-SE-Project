# Unit Test Report

**Project:** Task Manager Application  
**Sprint:** Sprint 2 — testing snapshot  
**Execution date:** 2 November 2026  
**Environment:** Windows 10/11, Python 3.11.9, pytest 8.3.4, pytest-cov 6.0.0  
**Branch:** `feature/s2-09-e2e-workflow`  
**Status:** Updated local test execution report; skipped scenarios remain pending.

## 1. Test execution

Full backend suite and coverage command:

```powershell
python -m pytest --cov=app --cov-branch --cov-report=term-missing --cov-report=json:coverage.json --junitxml=junit.xml
```

The JSON report was used to calculate the branch percentage:

```powershell
python -c "import json; t=json.load(open('coverage.json'))['totals']; print('Covered branches:', t['covered_branches'], '/', t['num_branches']); print('Branch coverage:', round(t['percent_branches_covered'], 2), '%')"
```

## 2. Overall backend results

| Test group | Passed | Skipped | Total |
|---|---:|---:|---:|
| Backend unit tests | 49 | 25 | 74 |
| Backend integration/API tests | 32 | 19 | 51 |
| **Backend total** | **81** | **44** | **125** |

**Failed:** 0

## 3. Unit-test file results

| Test file | Passed | Skipped |
|---|---:|---:|
| `tests/unit/test_auth_service.py` | 5 | 0 |
| `tests/unit/test_models.py` | 29 | 0 |
| `tests/unit/test_notification_service.py` | 15 | 0 |
| `tests/unit/test_search_service.py` | 0 | 7 |
| `tests/unit/test_task_rules.py` | 0 | 11 |
| `tests/unit/test_task_service.py` | 0 | 7 |
| **Total** | **49** | **25** |

## 4. Integration/API test file results

| Test file | Passed | Skipped |
|---|---:|---:|
| `tests/integration/test_admin_api.py` | 2 | 2 |
| `tests/integration/test_auth_api.py` | 8 | 0 |
| `tests/integration/test_categories_api.py` | 1 | 2 |
| `tests/integration/test_health_api.py` | 11 | 0 |
| `tests/integration/test_notifications_api.py` | 4 | 0 |
| `tests/integration/test_persistence.py` | 0 | 1 |
| `tests/integration/test_search_api.py` | 0 | 4 |
| `tests/integration/test_security_api.py` | 2 | 3 |
| `tests/integration/test_summary_api.py` | 1 | 2 |
| `tests/integration/test_tasks_api.py` | 3 | 5 |
| **Total** | **32** | **19** |

## 5. Notification and authentication test coverage

The 15 notification unit tests and 4 notification API tests passed. They exercise notification creation, user-scoped retrieval, read-state changes, validation, linked-task ownership, scheduling, provider outcomes and authorization.

The authentication unit and API tests are now active:
- `test_auth_service.py`: 5 passed.
- `test_auth_api.py`: 8 passed.

These cover credential verification, login, invalid credentials, logout, session invalidation and the current-user endpoint.

## 6. Coverage snapshot

| Metric | Result |
|---|---:|
| Statements | 646 |
| Missed statements | 78 |
| Statement coverage | 87.93% (approximately 88%) |
| Total branch paths | 92 |
| Covered branch paths | 66 |
| Branch coverage | 71.74% |

The separate Code Coverage and Branch Coverage reports document the calculation and interpretation.

## 7. Warnings and skipped tests

The run completed with **81 passed, 44 skipped, 0 failed**. Nine SQLAlchemy `LegacyAPIWarning` warnings were reported, primarily for existing `Query.get()` calls. They did not fail the tests.

The 44 skipped tests are pending coverage for incomplete task rules/services, search, persistence, category, admin, dashboard and related scenarios. A skipped test is not counted as passed.

## 8. Conclusion

The updated backend suite has 81 passing tests and no failures. Authentication and notification unit/API scenarios are active and passing. This is a testing snapshot, not final system sign-off, because 44 backend tests remain skipped and additional end-to-end scenarios are pending.
