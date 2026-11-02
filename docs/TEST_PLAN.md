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
- **TC-Notify-01:** Notification persistence, user-scoped listing, read-state changes, scheduled dispatch and provider delivery/failure handling
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

## TC-Notify-01 — Detailed Test Cases (Sprint 2 / S2-07)

| Test ID | Scenario | Expected Result | Test Level |
|---|---|---|---|
| TC-Notify-01a | Create a notification for an existing user | Record is persisted with pending status and UTC timestamp policy | Unit |
| TC-Notify-01b | List notifications as a user with own and foreign records present | Only the authenticated user's notifications are returned | Unit / Integration |
| TC-Notify-01c | Mark an owned notification as read | Status changes to read; repeated request remains successful | Unit / Integration |
| TC-Notify-01d | Mark another user's notification as read | API returns 404 without disclosing the foreign record | Unit / Integration |
| TC-Notify-01e | Submit empty or overlong notification message | ValidationError is raised; no record is created | Unit |
| TC-Notify-01f | Link a notification to another user's task | API/service rejects the operation as not found | Unit |
| TC-Notify-01g | Dispatch a notification before scheduled_at | Notification remains pending and provider is not called | Unit |
| TC-Notify-01h | Provider reports successful delivery | Status becomes delivered and delivered_at is recorded in UTC | Unit |
| TC-Notify-01i | Provider reports a delivery failure | Status becomes failed and delivered_at remains empty | Unit |
| TC-Notify-01j | Scheduler is stopped or not started | No queued notifications are dispatched | Unit |
| TC-Notify-01k | Scheduler is started and a queued notification is due | Provider is called and queue entry is removed | Unit |

## Performance and Environment Assumptions
- Normal operational load is 20 concurrent active users over the agreed 30-second test window.
- The target is p90 response time <= 3 seconds in the documented test environment.
- Scheduled timestamps are stored and compared as UTC. A stored SQLite timestamp without tzinfo is interpreted as UTC according to the project policy.
- No external delivery provider or default reminder interval is assumed. The scheduler is manually driven until the team approves a production scheduling mechanism.
