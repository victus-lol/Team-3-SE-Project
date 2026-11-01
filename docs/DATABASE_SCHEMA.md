# Database Schema

## Tables

### `users`
- `id`: INTEGER PRIMARY KEY AUTOINCREMENT
- `name`: VARCHAR(128) NOT NULL (CHECK length > 0)
- `email`: VARCHAR(254) NOT NULL UNIQUE (CHECK length >= 3 AND email LIKE '%@%')
- `password_hash`: VARCHAR(256) NOT NULL
- `role`: VARCHAR(10) NOT NULL DEFAULT 'user' (CHECK role IN ('user', 'admin'))
- `is_active`: BOOLEAN NOT NULL DEFAULT 1
- `created_at`: TIMESTAMP NOT NULL
- `updated_at`: TIMESTAMP NOT NULL

### `tasks`
- `id`: INTEGER PRIMARY KEY AUTOINCREMENT
- `owner_id`: INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
- `title`: VARCHAR(200) NOT NULL (CHECK length > 0 AND length <= 200)
- `description`: TEXT NULL
- `priority`: VARCHAR(10) NOT NULL DEFAULT 'medium' (CHECK priority IN ('low', 'medium', 'high'))
- `due_date`: DATE NULL
- `status`: VARCHAR(20) NOT NULL DEFAULT 'pending' (CHECK status IN ('pending', 'in_progress', 'completed'))
- `category_id`: INTEGER NULL REFERENCES categories(id) ON DELETE SET NULL
- `created_at`: TIMESTAMP NOT NULL
- `updated_at`: TIMESTAMP NOT NULL

### `categories`
- `id`: INTEGER PRIMARY KEY AUTOINCREMENT
- `user_id`: INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
- `name`: VARCHAR(100) NOT NULL (CHECK length > 0 AND length <= 100)
- `created_at`: TIMESTAMP NOT NULL
- `updated_at`: TIMESTAMP NOT NULL
- UNIQUE (user_id, name)

### `notifications`
- `id`: INTEGER PRIMARY KEY AUTOINCREMENT
- `user_id`: INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
- `task_id`: INTEGER NULL REFERENCES tasks(id) ON DELETE SET NULL
- `message`: VARCHAR(512) NOT NULL (CHECK length > 0)
- `scheduled_at`: TIMESTAMP NULL
- `delivered_at`: TIMESTAMP NULL
- `status`: VARCHAR(20) NOT NULL DEFAULT 'pending' (CHECK status IN ('pending', 'delivered', 'read', 'failed'))
- `created_at`: TIMESTAMP NOT NULL

