BEGIN;

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

CREATE INDEX idx_santiago_munoz_todo_is_completed ON santiago_munoz_todos(is_completed);
CREATE INDEX idx_santiago_munoz_todo_created_at ON santiago_munoz_todos(created_at DESC);
CREATE INDEX idx_santiago_munoz_todo_due_date ON santiago_munoz_todos(due_date ASC);

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

COMMIT;
