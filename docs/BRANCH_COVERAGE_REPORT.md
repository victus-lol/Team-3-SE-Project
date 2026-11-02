# Branch Coverage Report

**Project:** Task Manager Application  
**Execution date:** 2 November 2026  
**Branch:** `feature/s2-07-notifications`  
**Environment:** Windows, Python 3.11.9, Coverage.py via pytest-cov 6.0.0  
**Status:** Preliminary backend branch coverage snapshot.

## 1. Execution

Branch measurement was enabled with:

```powershell
python -m pytest --cov=app --cov-branch --cov-report=term-missing
python -m coverage json -o coverage.json
```

The branch percentage was calculated from the JSON totals:

```powershell
python -c "import json; t=json.load(open('coverage.json'))['totals']; print(round(t['covered_branches']/t['num_branches']*100,2)); print(t['covered_branches'], '/', t['num_branches'])"
```

## 2. Overall branch coverage

| Metric | Result |
|---|---:|
| Total branches | 78 |
| Covered branches | 54 |
| Uncovered branches | 24 |
| **Branch coverage** | **69.23%** |

Calculation:

`54 / 78 × 100 = 69.23%`

## 3. Interpretation

Branch coverage measures whether the possible outcomes of decision points (for example, true/false paths through conditional logic) were exercised during the test run. It is different from statement coverage.

The associated statement coverage was 85.32%. A higher statement percentage does not imply that every branch was tested.

## 4. Remaining work

The JSON report and terminal `term-missing` output identify branch opportunities not exercised by this test suite. The next testing pass should prioritize:
- Provider exceptions and failure handling.
- Future and due scheduled-notification paths.
- Scheduler queue behavior when records are deleted or already processed.
- Error and authorization branches in shared middleware.
- Pending branches in authentication, task, search and service modules once their skipped tests are implemented.

## 5. Limitations

- This measurement covers the backend Python package only.
- The run included 57 skipped tests; skipped tests contribute no executed branch coverage.
- The workflow CI command currently produces line coverage without the `--cov-branch` option; this branch figure is from the local Windows run.
- No minimum branch coverage threshold has been established in the available project documentation.

## 6. Conclusion

The measured backend branch coverage is **69.23% (54 of 78 branches)**. This is a preliminary result, not final test sign-off. Additional branch-focused tests are needed, especially in currently incomplete modules.
