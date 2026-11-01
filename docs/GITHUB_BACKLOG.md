# GitHub Backlog (Local Issue Definitions)

> **Notice:** These are local issue definitions and requirements. No remote GitHub issues or projects have been created.

## Sprint 1 Issues

### S1-01: Repository Setup, Structure, and Development Standards
- **Owner:** Akash Pawar
- **Component:** Infrastructure
- **Priority:** High
- **Points:** 3
- **Requirements:** TMA-SR-001
- **Description:** Establish project folder hierarchy, configuration files, gitignore, and development guidelines.
- **Acceptance Criteria:** Standard directory structure exists, no container files present, gitignore covers secrets and DB files.
- **Dependencies:** None
- **Test Requirements:** Manual directory check.
- **Definition of Done:** Documentation and tooling files committed to main.

### S1-02: Flask App Setup, SQLite Connection, and Migrations
- **Owner:** Balaji Gowda S R
- **Component:** Backend Core
- **Priority:** High
- **Points:** 5
- **Requirements:** TMA-SR-001
- **Description:** Implement application factory `create_app()`, configure SQLite with PRAGMA foreign keys and WAL, wire Flask-Migrate.
- **Acceptance Criteria:** `flask db upgrade` executes cleanly; test DB isolated from dev DB.
- **Dependencies:** S1-01
- **Test Requirements:** `test_health_api.py::test_ready_endpoint`, `test_db_isolation`.
- **Definition of Done:** Health endpoints return 200, SQLite connected.

### S1-03: User Model, Password Hashing, Authentication, and Sessions
- **Owner:** Balaji Gowda S R
- **Component:** Backend Auth
- **Priority:** High
- **Points:** 8
- **Requirements:** TMA-F-001, TMA-F-002, TMA-SR-001, TMA-SR-003
- **Description:** Create User model, Werkzeug hashing, Flask-Login user loader, login/logout routes, and CLI admin command.
- **Acceptance Criteria:** Plaintext passwords never stored, invalid login returns 401, logout clears session.
- **Dependencies:** S1-02
- **Test Requirements:** TC-Auth-01, TC-Auth-02, TC-Auth-03 in `test_auth_api.py`.
- **Definition of Done:** User model tested; auth endpoints fully operational.

### S1-04: Task Model, CRUD APIs, and Validation
- **Owner:** Aadi Kore
- **Component:** Backend Tasks
- **Priority:** High
- **Points:** 8
- **Requirements:** TMA-F-010, TMA-F-011, TMA-F-012
- **Description:** Implement Task model, validation schemas, and REST endpoints for task CRUD.
- **Acceptance Criteria:** Valid payload creates task; empty title returns 400; category ownership validated.
- **Dependencies:** S1-02, S1-03
- **Test Requirements:** TC-Task-01, TC-Task-02, TC-Task-03 in `test_tasks_api.py`.
- **Definition of Done:** All CRUD endpoints functional and tested.

### S1-05: Task Ownership and Authorization Rules
- **Owner:** Aadi Kore
- **Component:** Backend Security
- **Priority:** High
- **Points:** 5
- **Requirements:** TMA-SR-001
- **Description:** Enforce server-side task ownership checks so users cannot view or mutate other users' tasks.
- **Acceptance Criteria:** Accessing another user's task returns 404.
- **Dependencies:** S1-04
- **Test Requirements:** TC-Sec-01 in `test_tasks_api.py`.
- **Definition of Done:** Automated test proves cross-user task access returns 404.

### S1-06: React Vite Setup, Routing, and Frontend Layout
- **Owner:** Aaryan Dubey
- **Component:** Frontend Foundation
- **Priority:** High
- **Points:** 5
- **Requirements:** TMA-F-001
- **Description:** Set up Vite React application, React Router, global CSS, layout components, and API proxy.
- **Acceptance Criteria:** App shell renders; proxy routes `/api` to Flask.
- **Dependencies:** None
- **Test Requirements:** `Foundation.test.jsx`.
- **Definition of Done:** React builds cleanly and passes Vitest.

### S1-07: Login Interface, Session Management, and Protected Routes
- **Owner:** Aaryan Dubey
- **Component:** Frontend Auth
- **Priority:** High
- **Points:** 8
- **Requirements:** TMA-F-001, TMA-F-002
- **Description:** Build LoginPage, AuthContext, ProtectedRoute, and session verification via `/api/auth/me`.
- **Acceptance Criteria:** Form validates inputs; redirects to requested route upon successful login.
- **Dependencies:** S1-03, S1-06
- **Test Requirements:** `LoginPage.test.jsx`.
- **Definition of Done:** Complete login and logout flow working in UI.

### S1-08: Task List, Form, Edit, and Delete Integration
- **Owner:** Aaryan Dubey
- **Component:** Frontend Tasks
- **Priority:** High
- **Points:** 8
- **Requirements:** TMA-F-010, TMA-F-011, TMA-F-012
- **Description:** Implement TaskList, TaskCard, TaskForm, and deletion ConfirmDialog.
- **Acceptance Criteria:** Authenticated user can create, view, update, and delete tasks in the UI.
- **Dependencies:** S1-04, S1-05, S1-07
- **Test Requirements:** `TaskList.test.jsx`, `TaskForm.test.jsx`.
- **Definition of Done:** Interactive task management working against Flask API.

### S1-09: Testing Infrastructure, Fixtures, and Seed-Data Setup
- **Owner:** Akash Pawar
- **Component:** QA / Infra
- **Priority:** Medium
- **Points:** 5
- **Requirements:** TMA-NF-001
- **Description:** Set up pytest conftest, isolated SQLite fixture, seed.py, reset_test_data.py, and pending check script.
- **Acceptance Criteria:** Fixtures isolate test DB from dev DB; seed script populates sample records.
- **Dependencies:** S1-02
- **Test Requirements:** `test_health_api.py::test_db_isolation`.
- **Definition of Done:** Test suites run reliably and cleanly.

### S1-10: GitHub Actions CI, PR Template, and Quality Checks
- **Owner:** Akash Pawar
- **Component:** DevOps
- **Priority:** Medium
- **Points:** 5
- **Requirements:** TMA-SR-001
- **Description:** Create GitHub Actions CI workflow for backend and frontend linting, tests, and pending inventory checks.
- **Acceptance Criteria:** CI runs on PR and push; blocks merges on test failure.
- **Dependencies:** S1-01
- **Test Requirements:** Run workflows locally or validate yaml syntax.
- **Definition of Done:** Workflows committed and validated.

---

## Sprint 2 Issues

### S2-01: Priority, Due Date, Status, and Category Rules
- **Owner:** Aadi Kore | **Points:** 5 | **Requirements:** TMA-F-020, TMA-F-030
### S2-02: Search, Multi-Field Filtering, Sorting, and Overdue Detection
- **Owner:** Aadi Kore | **Points:** 8 | **Requirements:** TMA-F-021, TMA-F-022, TMA-F-023
### S2-03: Frontend Organization and Search/Filter UI
- **Owner:** Aaryan Dubey | **Points:** 5 | **Requirements:** TMA-F-021, TMA-F-022
### S2-04: Dashboard Summary API
- **Owner:** Balaji Gowda S R | **Points:** 5 | **Requirements:** TMA-F-033
### S2-05: Dashboard Interface and Summary Cards
- **Owner:** Aaryan Dubey | **Points:** 5 | **Requirements:** TMA-F-033
### S2-06: Admin APIs and Role-Based Authorization
- **Owner:** Balaji Gowda S R | **Points:** 5 | **Requirements:** TMA-SR-001
### S2-07: Notification Service, Scheduler, and Test Provider
- **Owner:** Akash Pawar | **Points:** 8 | **Requirements:** TMA-F-040, TMA-F-041, TMA-F-042
### S2-08: Notification Interface
- **Owner:** Aaryan Dubey | **Points:** 5 | **Requirements:** TMA-F-040, TMA-F-041
### S2-09: End-to-End Testing and Workflow Integration
- **Owner:** Akash Pawar | **Points:** 8 | **Requirements:** TMA-NF-001
### S2-10: Security, Performance, and Persistence Regression Testing
- **Owner:** Aadi Kore & Akash Pawar | **Points:** 5 | **Requirements:** TMA-NF-002, TMA-SR-003
### S2-11: Requirement Traceability Matrix and Test Documentation
- **Owner:** Aadi Kore | **Points:** 3 | **Requirements:** TMA-NF-001
### S2-12: Responsive UI, Accessibility, and Final Frontend Polish
- **Owner:** Aaryan Dubey | **Points:** 5 | **Requirements:** TMA-NF-005

