BEGIN;

CREATE SCHEMA IF NOT EXISTS santiago_munoz_write;

CREATE TYPE santiago_munoz_write.todo_priority AS ENUM ('Low', 'Medium', 'High');

CREATE TABLE santiago_munoz_write.todos (
    id UUID PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description VARCHAR(500),
    priority santiago_munoz_write.todo_priority,
    due_date TIMESTAMPTZ,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Idempotency tracking
CREATE TABLE santiago_munoz_write.processed_commands (
    command_id UUID PRIMARY KEY,
    result_status INTEGER NOT NULL,
    result_body JSONB,
    processed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Outbox for CQRS events
CREATE TABLE santiago_munoz_write.outbox (
    id BIGSERIAL PRIMARY KEY,
    aggregate_id UUID NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    published_at TIMESTAMPTZ
);

COMMIT;
