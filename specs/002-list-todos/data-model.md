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

## Database Schema (Shared)

The Read Side queries directly from the Write Side tables.

| Table Name | Description |
|------------|-------------|
| `santiago_munoz_todos` | Primary table for task data |

```sql
-- Existing Write Side table used for Read queries
CREATE TABLE santiago_munoz_todos (
    id UUID PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description VARCHAR(500),
    priority santiago_munoz_todo_priority,
    due_date TIMESTAMPTZ,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes optimized for queries
CREATE INDEX idx_santiago_munoz_todo_is_completed ON santiago_munoz_todos(is_completed);
CREATE INDEX idx_santiago_munoz_todo_created_at ON santiago_munoz_todos(created_at DESC);
CREATE INDEX idx_santiago_munoz_todo_due_date ON santiago_munoz_todos(due_date ASC);
```

## State Mappings
- `status=completed` -> `WHERE is_completed = TRUE`
- `status=pending` -> `WHERE is_completed = FALSE`
- `sort=created_at` -> `ORDER BY created_at`
- `sort=due_date` -> `ORDER BY due_date`
