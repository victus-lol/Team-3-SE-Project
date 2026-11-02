# Decisions and Open Questions Register

## 1. User Registration Scope
- **Status:** Open / Scope-Pending
- **Assumption:** Public self-registration is deferred pending business review. Administrator accounts bootstrap using `flask create-admin`. Public registration route `POST /api/auth/register` returns `501 NOT_IMPLEMENTED`.
- **Impact:** System currently operates via invitation/admin-provisioning.

## 2. Category Management Scope
- **Status:** Open / Scope-Pending
- **Assumption:** Categories are user-scoped with case-insensitive unique names per user. Creation API `POST /api/categories` returns `501` until final UI requirements are confirmed.
- **Impact:** Seed data provides initial categories for development.

## 3. Reminder Schedule and Delivery Mechanism
- **Status:** Open — production decision pending
- **Assumption:** No external notification infrastructure (e.g. Twilio, SendGrid) or default reminder interval is assumed. In-app notifications are persisted to the database. The S2-07 implementation provides an explicit, manually driven scheduler queue and provider interface; it does not start a background thread or timer automatically. Tests inject `FakeNotificationProvider` and call the scheduler explicitly.
- **Impact:** Tests verify notification record creation, ownership, read state, due-time handling and provider delivery state transitions without external network calls. A production polling/worker mechanism and reminder policy require a separate team decision.

## 4. Date/Time and Timezone Policy
- **Status:** Decided (Provisional)
- **Assumption:** All database timestamps (`created_at`, `updated_at`, `scheduled_at`, `delivered_at`) are stored in UTC. Task deadlines use SQL `DATE` (`YYYY-MM-DD`). Overdue calculations evaluate deadlines against current date in `APP_TIMEZONE` (fallback to UTC).
- **Impact:** Eliminates timezone ambiguity across server and database operations.

## 5. Admin Operations and Visibility
- **Status:** Decided
- **Assumption:** Standard users receive `403 FORBIDDEN` when accessing `/api/admin/*`. Attempting to access other users' tasks returns `404 NOT_FOUND` rather than `403` to prevent ID enumeration.
- **Impact:** Tight access control and information leak prevention.

## 6. Normal Performance Load Definition
- **Status:** Decided (Provisional)
- **Assumption:** Normal operational load is defined as 20 concurrent active users with a target response latency of p90 <= 3 seconds.
- **Impact:** Load test scenario in `tests/performance/tasks-load.js` models 20 virtual users over a 30-second window.

## 7. Availability and Deployment Environment
- **Status:** Open
- **Assumption:** Single-instance SQLite deployment with WAL mode enabled.
- **Impact:** Horizontal scale-out is not supported on raw SQLite without distributed storage extensions.

## 8. Production Hosting and HTTPS
- **Status:** Decided
- **Assumption:** Reverse proxy terminates TLS; Flask enforces secure cookies (`SESSION_COOKIE_SECURE = True`) in production mode.
- **Impact:** `SECRET_KEY` must be explicitly configured in production; missing key fails fast on startup.
