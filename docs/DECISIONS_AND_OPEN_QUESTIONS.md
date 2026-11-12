# Decisions and Open Questions

**Reviewed:** 12 November 2026

## Decided

1. **Registration:** Public registration creates standard users only. Admin accounts are provisioned with the Flask `create-admin` CLI. Registration cannot assign roles.
2. **Categories:** Categories belong to a user; names are normalized and unique per user.
3. **Authorization:** Admin endpoints require an admin role. Access to another user's task/category/notification is hidden as 404 where applicable.
4. **Passwords and recovery:** Passwords use Werkzeug hashes. Reset tokens are random, single-use, time-limited, and stored as hashes. Reset increments the user's session version to invalidate existing sessions.
5. **CSRF and sessions:** Browser requests use the session cookie and X-CSRFToken. Production enables secure cookies; the reverse proxy is expected to terminate TLS.
6. **Dates:** Stored timestamps use UTC. Task deadlines are dates and overdue evaluation uses the configured application timezone.
7. **Load target:** Test 20 authenticated users for 30 seconds and keep p90 under 3 seconds. The latest local Windows/SQLite run on 12 November measured 172.89 ms p90; see `docs/TEST_PLAN.md` for the full result and limits.
8. **Persistence:** SQLite with WAL is supported for the current single-instance project. The automated regression test verifies persistence after closing/reopening a session on the same file-backed database.

## Open operational questions

1. **Mail delivery:** A deployment owner must configure SMTP host/port/credentials/from address and `PUBLIC_APP_URL`. No SMTP credentials are committed. Tests stub delivery; they do not send real mail.
2. **Notification production worker:** The scheduler is manually driven and the provider is injectable. Select a worker and production delivery provider before claiming automated production reminders.
3. **Hosting:** No hosting provider is selected. CI produces a versioned GitHub Release bundle; it does not deploy a live application.
4. **Database at scale:** Select a managed database before horizontal scaling; this repository's SQLite setup is for a single instance.
