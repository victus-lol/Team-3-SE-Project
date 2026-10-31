# SQLite Usage Guidelines

## Connection Configuration
1. **Foreign Key Enforcement:** Explicitly enabled on every connection via:
   ```sql
   PRAGMA foreign_keys = ON;
   ```
2. **Busy Timeout:** Configured to `5000` ms to handle concurrent reads/writes cleanly.
3. **Write-Ahead Logging (WAL):** Enabled for file-based database instances (`PRAGMA journal_mode=WAL;`). In-memory databases used in testing bypass WAL.

## Isolation Rules
- Automated tests run against separate temporary databases or in-memory instances.
- Tests assert that the database URI never touches `task_manager.sqlite`.

