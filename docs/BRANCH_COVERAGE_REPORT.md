# Backend Branch Coverage Report

**Execution date:** 12 November 2026
**Environment:** Windows, Python 3.12.6, pytest-cov / Coverage.py
**Test result:** 167 passed, 0 skipped, 0 failed

Branch coverage was measured with `python -m pytest --cov=app --cov-branch --cov-report=json:coverage.json --cov-report=term -q` from `server/`.

| Metric | Result |
|---|---:|
| Branch paths | 298 |
| Covered branch paths | 191 |
| Uncovered branch paths | 107 |
| **Branch coverage** | **64.09%** |

Calculation: 191 / 298 x 100 = 64.09%. Statement coverage for the same run was 84.69%. Coverage.py's combined value was 80.80%; see `docs/CODE_COVERAGE_REPORT.md` for the distinction.

The remaining uncovered paths are concentrated in SMTP delivery, schema validation edges, search filters, authorization/error alternatives, and app configuration. SMTP delivery is intentionally tested through a stub; no real SMTP credentials are available in this environment.
