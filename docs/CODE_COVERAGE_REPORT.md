# Code Coverage Report

**Project:** Task Manager Application  
**Execution date:** 2 November 2026  
**Branch:** `feature/s2-07-notifications`  
**Environment:** Windows, Python 3.11.9, Coverage.py via pytest-cov 6.0.0  
**Status:** Preliminary backend coverage snapshot.

## 1. Execution commands

```powershell
python -m pytest --cov=app --cov-branch --cov-report=term-missing
python -m coverage json -o coverage.json
```

Statement coverage was calculated from the JSON totals:

```powershell
python -c "import json; t=json.load(open('coverage.json'))['totals']; print(round(t['covered_lines']/t['num_statements']*100,2))"
```

## 2. Overall statement coverage

| Metric | Result |
|---|---:|
| Covered statements/lines | 523 / 613 |
| Missed statements/lines | 90 |
| **Statement coverage** | **85.32%** |

The 84% shown in the terminal's `TOTAL Cover` column is Coverage.py's combined score when branch measurement is enabled. The 85.32% value above is the line/statement percentage calculated separately from the JSON totals.

## 3. Notification module coverage

| Module | Statements | Missed | Displayed coverage |
|---|---:|---:|---:|
| `app/models/notification.py` | 19 | 1 | 95% |
| `app/notifications/provider.py` | 13 | 2 | 85% |
| `app/notifications/routes.py` | 16 | 0 | 100% |
| `app/notifications/scheduler.py` | 41 | 2 | 94% |
| `app/notifications/service.py` | 68 | 8 | 86% |

The five notification-related modules contain 157 statements, of which 144 were executed in this run (91.72% when aggregated by statement count). The displayed per-file values are rounded by Coverage.py.

## 4. Interpretation

The notification routes reached 100% displayed statement coverage. The service, provider and scheduler still have statements not exercised by this test run; their missing-line details are listed in the terminal coverage output.

Coverage indicates which code was executed during this test run. It does not prove that every possible input, integration, timing condition or production scenario is correct.

## 5. Limitations

- This is backend coverage only; it does not include React/Vitest or Playwright coverage.
- 57 backend tests were skipped in the associated run.
- The report represents the Windows/Python 3.11.9 execution on this feature branch. CI uses a separate Linux/Python 3.12 environment.
- No project-wide minimum coverage threshold is asserted here.

## 6. Conclusion

The observed backend statement coverage is **85.32%**. The notification module statement coverage is high overall, with the route module at 100% displayed coverage. Remaining gaps and skipped tests should be considered during the final test cycle.
