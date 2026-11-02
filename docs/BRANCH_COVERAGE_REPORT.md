# Branch Coverage Report

**Project:** Task Manager Application  
**Execution date:** 2 November 2026  
**Branch:** `feature/s2-09-e2e-workflow`  
**Environment:** Windows, Python 3.11.9, Coverage.py via pytest-cov 6.0.0  
**Status:** Updated local backend branch coverage snapshot.

## 1. Execution

Branch measurement was enabled with:

```powershell
python -m pytest --cov=app --cov-branch --cov-report=term-missing --cov-report=json:coverage.json --junitxml=junit.xml
```

The branch percentage was calculated from Coverage.py's JSON totals:

```powershell
python -c "import json; t=json.load(open('coverage.json'))['totals']; print('Covered branches:', t['covered_branches'], '/', t['num_branches']); print('Branch coverage:', round(t['percent_branches_covered'], 2), '%')"
```

## 2. Overall branch coverage

| Metric | Result |
|---|---:|
| Total branches | 92 |
| Covered branches | 66 |
| Uncovered branches | 26 |
| **Branch coverage** | **71.74%** |

Calculation:

`66 / 92 × 100 = 71.739...% ≈ 71.74%`

The terminal report lists 20 partially covered source lines in its `BrPart` column. This is a count of lines with partial branch execution, not the number of uncovered branch paths. The total uncovered branch paths are 26 (92 total minus 66 covered).

## 3. Interpretation

Branch coverage measures whether the possible outcomes of decision points (for example, true and false paths through conditional logic) were exercised during the test run. It differs from statement coverage.

The same run measured 568 of 646 statements covered (87.93%, approximately 88%). Coverage.py's terminal `Cover` column showed 86% because branch measurement was enabled and that column combines statement and branch coverage. The separate percentages should not be treated as interchangeable.

## 4. Areas for additional branch testing

The terminal output indicates remaining paths in:
- Authorization middleware and permission/role decisions.
- Authentication controller and service validation/error outcomes.
- Shared response and error-handling paths.
- Notification provider failures and scheduler timing/queue conditions.
- Application configuration and initialization alternatives.

The generated `coverage.json` contains the detailed file-level branch totals and uncovered branch locations for follow-up test design.

## 5. Associated test results

The branch snapshot was produced by a backend run with **81 passed, 44 skipped and 0 failed** (125 collected tests). Skipped tests contribute no executed branch coverage.

## 6. Limitations

- This measurement covers the backend Python package only.
- Frontend and Playwright browser tests are reported separately.
- The measurement is from Windows/Python 3.11.9. CI uses Linux/Python 3.12 and reports line coverage; the CI job does not currently enable `--cov-branch`.
- No minimum branch coverage threshold has been established in the available project test plan.

## 7. Conclusion

The measured local backend branch coverage is **71.74% (66 of 92 branch paths)**. Further branch-focused tests are recommended for authorization, validation, error handling and notification scheduling. This remains a preliminary result, not final test sign-off.
