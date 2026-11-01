# Test Plan

## Test Strategy
- **Unit Tests:** Validate individual service methods, rules, models, and UI components in complete isolation.
- **Integration Tests:** Verify full HTTP request/response lifecycles, database transactions, and authorization decorators.
- **E2E Tests:** End-to-end browser workflows using Playwright against live development instances of backend and frontend.

## Case IDs & Coverage Mapping
- **TC-Auth-01:** Valid authentication and session establishment
- **TC-Auth-02:** Invalid credentials rejection
- **TC-Auth-03:** Logout and session invalidation
- **TC-Task-01:** Task creation and owner scoping
- **TC-Task-02:** Updating owned tasks
- **TC-Task-03:** Confirmed task deletion
- **TC-Org-01:** Priority validation
- **TC-Org-02:** Due date validation
- **TC-Org-03:** Status state transitions
- **TC-Org-04:** Category scoping and allocation
- **TC-Search-01:** Keyword search over title and description
- **TC-Search-02:** Multi-field filtering
- **TC-Search-03:** Deterministic sorting
- **TC-Monitor-01:** Overdue task identification
- **TC-Notify-01:** Reminder generation and notification delivery
- **TC-Summary-01:** Dashboard counts aggregation
- **TC-Admin-01:** Role-based access control and admin operations
- **TC-Perf-01:** p90 <= 3s under normal agreed load (20 concurrent users)
- **TC-Rel-01:** Service availability
- **TC-Data-01:** Data persistence across application restart
- **TC-UX-01:** Frontend accessibility and responsiveness
- **TC-Sec-01:** Unauthenticated access rejected
- **TC-Sec-02:** Standard user rejected from admin endpoints
- **TC-Sec-03:** Password hashes excluded from API responses
- **TC-Sec-04:** Transport and cookie protection
- **TC-Sec-05:** Hostile input sanitized and rejected

