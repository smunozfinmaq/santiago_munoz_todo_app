# Data Model: US-001: Create Todo

## Entities

### Todo (Aggregate Root)
Represented in `write/src/domain/model.py`.

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| `id` | UUID | Primary Key | Unique identifier |
| `title` | String | Max 500, Not Null | Task summary |
| `description`| String | Max 500, Nullable | Detailed notes |
| `priority` | Enum | Low, Medium, High | Task importance |
| `due_date` | Timestamp | ISO-8601, Nullable | Deadline |
| `is_completed`| Boolean | Default False | Status |
| `created_at` | Timestamp | Not Null | Audit |
| `updated_at` | Timestamp | Not Null | Audit |

## Database Schema (Write Side)

```sql
CREATE TYPE santiago_munoz_todo_priority AS ENUM ('Low', 'Medium', 'High');

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

-- Idempotency tracking
CREATE TABLE santiago_munoz_processed_commands (
    command_id UUID PRIMARY KEY,
    result_status INTEGER NOT NULL,
    result_body JSONB,
    processed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Outbox for CQRS events
CREATE TABLE santiago_munoz_outbox (
    id BIGSERIAL PRIMARY KEY,
    aggregate_id UUID NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    published_at TIMESTAMPTZ
);
```

## State Transitions
1. **Creation**: `(None) -> Created`. Sets `is_completed = false` and generates IDs.
