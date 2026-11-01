# Testing Guide & Commands

## Running Backend Tests
```bash
cd server
pytest -v
pytest --cov=app --cov-report=term-missing
```

## Running Frontend Tests
```bash
cd client
npm test
npm run test:coverage
```

## Running Inventory of Pending Test Placeholders
```bash
python scripts/check_test_placeholders.py
```

To run with strict release gating (fails if ANY test is still pending):
```bash
python scripts/check_test_placeholders.py --fail-on-pending
```

## Running E2E Smoke Tests
```bash
npx playwright test
```

