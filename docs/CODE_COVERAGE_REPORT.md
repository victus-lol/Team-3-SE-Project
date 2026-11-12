# Backend Statement Coverage Report

**Execution date:** 12 November 2026
**Environment:** Windows, Python 3.12.6, pytest-cov / Coverage.py
**Test result:** 167 passed, 0 skipped, 0 failed

## Command

```powershell
cd server
python -m pytest --cov=app --cov-branch --cov-report=term --cov-report=json:coverage.json -q
```

## Measured coverage

| Metric | Result |
|---|---:|
| Statements | 1,280 |
| Covered statements | 1,084 |
| Missed statements | 196 |
| **Statement coverage** | **84.69%** |
| Branches | 298 |
| Covered branches | 191 |
| **Branch coverage** | **64.09%** |
| Coverage.py combined report | 80.80% |

Calculations: 1,084 / 1,280 = 84.69% statement coverage; 191 / 298 = 64.09% branch coverage. The combined value weights statements and branches together and must not be presented as statement-only coverage.

## Interpretation and limits

This measures Python backend execution only. It does not count React/Vitest or browser coverage. Lower-coverage areas include task schemas, authorization edge paths, search validation, SMTP transport, and error handling. SMTP transport is isolated from tests; no real email is sent. These figures are a local measurement; CI will independently publish its coverage summary and enforce the project quality threshold.
