# Release Checklist & Quality Gates

## Release Gates (Must Pass Before Merge/Release)

### 1. Zero Pending Required Tests
- [ ] Run `python scripts/check_test_placeholders.py --fail-on-pending`.
- [ ] Confirm exit code is 0 and no skipped tests remain for targeted features.

### 2. CI Pipeline Green
- [ ] Backend workflow passed: Ruff linting clean, Pytest 100% pass rate, coverage threshold met.
- [ ] Frontend workflow passed: ESLint clean, Vitest passing, production build succeeded.
- [ ] Security audit clean: `pip-audit` and `npm audit` report zero high/critical vulnerabilities.

### 3. Database Migrations Verified
- [ ] `flask db upgrade` succeeds from empty schema to latest revision.
- [ ] All table constraints, CHECKs, and foreign keys active and tested.

### 4. Security & Configuration
- [ ] `SECRET_KEY` set to cryptographically secure value (not development default).
- [ ] Database isolated and not exposed in public repositories.
- [ ] `instance/task_manager.sqlite` excluded by `.gitignore`.
- [ ] CORS/Proxy restricted: No wildcard origins.
- [ ] Passwords hashed with PBKDF2/SHA256; no plaintexts in logs or responses.

### 5. Final Sign-off
- [ ] Balaji Gowda S R (Backend, Auth, Security)
- [ ] Aaryan Dubey (Frontend, UI/UX)
- [ ] Aadi Kore (Business Logic, QA Lead)
- [ ] Akash Pawar (Infrastructure, Release Coordinator)

