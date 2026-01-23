BEGIN;

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

CREATE INDEX idx_read_todos_is_completed ON santiago_munoz_read.todos(is_completed);
CREATE INDEX idx_read_todos_created_at ON santiago_munoz_read.todos(created_at DESC);
CREATE INDEX idx_read_todos_due_date ON santiago_munoz_read.todos(due_date ASC);

CREATE TABLE santiago_munoz_read.processed_events (
    event_id UUID PRIMARY KEY,
    processed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMIT;
