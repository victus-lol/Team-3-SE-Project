# Requirement Traceability Matrix (RTM)

| Req ID | Description | Owner | Backend Module | Frontend Module | Test File | Issue ID | Status |
|---|---|---|---|---|---|---|---|
| TMA-F-001 | User Login & Authentication | Balaji / Aaryan | `app/auth/` | `features/auth/` | `test_auth_api.py` | S1-03, S1-07 | Not Started |
| TMA-F-002 | User Logout | Balaji / Aaryan | `app/auth/` | `features/auth/` | `test_auth_api.py` | S1-03, S1-07 | Not Started |
| TMA-F-010 | Task Creation & Retrieval | Aadi / Aaryan | `app/tasks/` | `features/tasks/` | `test_tasks_api.py` | S1-04, S1-08 | Not Started |
| TMA-F-011 | Task Update | Aadi / Aaryan | `app/tasks/` | `features/tasks/` | `test_tasks_api.py` | S1-04, S1-08 | Not Started |
| TMA-F-012 | Task Deletion | Aadi / Aaryan | `app/tasks/` | `features/tasks/` | `test_tasks_api.py` | S1-04, S1-08 | Not Started |
| TMA-F-020 | Priority & Status Rules | Aadi | `app/tasks/rules.py` | `features/tasks/` | `test_task_rules.py` | S2-01 | Not Started |
| TMA-F-021 | Task Search & Filtering | Aadi / Aaryan | `app/search/` | `features/search/` | `test_search_api.py` | S2-02, S2-03 | Not Started |
| TMA-F-022 | Overdue Task Detection | Aadi | `app/tasks/rules.py` | `features/search/` | `test_task_rules.py` | S2-02 | Not Started |
| TMA-F-023 | Deterministic Sorting | Aadi | `app/search/` | `features/search/` | `test_search_api.py` | S2-02 | Not Started |
| TMA-F-030 | Category Association | Aadi | `app/categories/` | `features/tasks/` | `test_categories_api.py` | S2-01 | Not Started |
| TMA-F-031 | Category Creation | Aadi | `app/categories/` | `features/tasks/` | `test_categories_api.py` | S2-01 | Not Started |
| TMA-F-033 | Dashboard Task Metrics | Balaji / Aaryan | `app/dashboard/` | `features/dashboard/` | `test_summary_api.py` | S2-04, S2-05 | Not Started |
| TMA-F-040 | Notification Generation | Akash / Aaryan | `app/notifications/`| `features/notifications/` | `test_notifications_api.py`| S2-07, S2-08 | Not Started |
| TMA-F-041 | Notification Status (Read) | Akash / Aaryan | `app/notifications/`| `features/notifications/` | `test_notifications_api.py`| S2-07, S2-08 | Not Started |
| TMA-F-042 | Notification Provider Abstraction | Akash | `app/notifications/provider.py` | N/A | `test_notification_service.py` | S2-07 | Not Started |
| TMA-SR-001 | Role-based Authorization | Balaji / Akash | `app/middleware/` | `components/ProtectedRoute.jsx`| `test_admin_api.py` | S1-05, S2-06 | Not Started |
| TMA-SR-003 | Secure Transport & Hashing | Balaji | `models/user.py` | N/A | `test_models.py` | S1-03, S2-10 | Not Started |
| TMA-SR-005 | Input Sanitization & Validation | Aadi / Balaji | `app/tasks/schemas.py`| `services/api.js` | `test_security_api.py` | S2-10 | Not Started |
| TMA-NF-001 | Persistence Across Restart | Akash / Aadi | Database config | N/A | `test_persistence.py` | S2-10 | Not Started |
| TMA-NF-002 | Response Time (p90 <= 3s) | Akash / Aadi | Whole API | UI | `tasks-load.js` | S2-10 | Not Started |
| TMA-NF-005 | Responsive Design & Accessibility| Aaryan | N/A | `styles/global.css` | Vitest / Playwright | S2-12 | Not Started |

