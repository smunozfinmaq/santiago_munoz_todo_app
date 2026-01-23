# Data Model: US-002: List Todos

## Entities (Read Side)

### TodoQueryModel
The read-side representation of a Todo.

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary Key |
| `title` | String | Task summary |
| `description`| String | Detailed notes |
| `priority` | Enum | Low, Medium, High |
| `due_date` | Timestamp | ISO-8601 |
| `is_completed`| Boolean | Status |
| `created_at` | Timestamp | Audit |
| `updated_at` | Timestamp | Audit |

## Database Schema (Read Side)

```sql
CREATE SCHEMA IF NOT EXISTS santiago_munoz_read;

CREATE TABLE santiago_munoz_read.todos (
    id UUID PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description VARCHAR(500),
    priority VARCHAR(20),
    due_date TIMESTAMPTZ,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

-- Indexes for performance
CREATE INDEX idx_read_todos_is_completed ON santiago_munoz_read.todos(is_completed);
CREATE INDEX idx_read_todos_created_at ON santiago_munoz_read.todos(created_at DESC);
CREATE INDEX idx_read_todos_due_date ON santiago_munoz_read.todos(due_date ASC);

-- Event tracking for projections
CREATE TABLE santiago_munoz_read.processed_events (
    event_id UUID PRIMARY KEY,
    processed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

## State Mappings
- `status=completed` -> `WHERE is_completed = TRUE`
- `status=pending` -> `WHERE is_completed = FALSE`
- `sort=created_at` -> `ORDER BY created_at`
- `sort=due_date` -> `ORDER BY due_date`
