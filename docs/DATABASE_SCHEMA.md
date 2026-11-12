# Database Schema

The current schema is defined by the SQLAlchemy models in `server/app/models/` and all migrations in `server/migrations/versions/`. Always apply migrations with `flask --app run.py db upgrade`; the initial migration alone does not contain the full current schema.

## Tables

### `users`
- `id`: integer primary key
- `name`: string(128), required
- `email`: string(254), required, unique and normalized to lowercase
- `password_hash`: string(256), required; plaintext password is never stored
- `role`: string(10), required, `user` or `admin`; public registration creates `user`
- `is_active`: boolean, required, default true
- `session_version`: integer, required, default 0; password reset increments it to invalidate old sessions
- `created_at`, `updated_at`: timestamps, required

### `tasks`
- `id`: integer primary key
- `owner_id`: required foreign key to `users.id`, cascade on user deletion
- `title`: string(200), required
- `description`: text, optional
- `priority`: string(10), `low`, `medium`, or `high`
- `due_date`: date, optional
- `status`: string(20), `pending`, `in_progress`, or `completed`
- `category_id`: optional foreign key to `categories.id`, set null on category deletion
- `created_at`, `updated_at`: timestamps, required

### `categories`
- `id`: integer primary key
- `user_id`: required foreign key to `users.id`, cascade on user deletion
- `name`: string(100), required
- `created_at`, `updated_at`: timestamps, required
- Unique constraint on `(user_id, name)`

### `notifications`
- `id`: integer primary key
- `user_id`: required foreign key to `users.id`, cascade on user deletion
- `task_id`: optional foreign key to `tasks.id`, set null on task deletion
- `message`: string(512), required
- `scheduled_at`, `delivered_at`: optional timestamps
- `status`: string(20), `pending`, `delivered`, `read`, or `failed`
- `created_at`: timestamp, required

### `login_attempts`
- `key_hash`: 64-character primary key; hashes the normalized account and client key
- `failure_count`: integer, required, default 0
- `window_started_at`: Unix timestamp, required
- `locked_until`: optional Unix timestamp

### `password_reset_tokens`
- `id`: integer primary key
- `user_id`: required foreign key to `users.id`, cascade on user deletion
- `token_hash`: string(64), required and unique; raw reset tokens are never stored
- `expires_at`: Unix timestamp, required
- `used_at`: optional Unix timestamp
- `created_at`: Unix timestamp, required

### `audit_logs`
- `id`: integer primary key
- `actor_id`: optional foreign key to `users.id`, set null on user deletion
- `action`: string(80), required
- `target_type`, `target_id`: optional strings(80)
- `created_at`: timestamp, required

## Operational notes

- Alembic migrations add the login throttling, audit logging, password reset, and session version fields.
- Automated and local tests use isolated databases. Do not use the development database as performance evidence.
- Password reset email delivery requires SMTP configuration; automated tests use a stub mail provider.
- Login throttling stores a keyed hash of account/client identity rather than raw account or address values.
- The database contains no plaintext passwords or password-reset tokens. Session invalidation uses `users.session_version`.
