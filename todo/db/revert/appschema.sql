BEGIN;

DROP TABLE outbox;
DROP TABLE processed_commands;
DROP TABLE todos;
DROP TYPE todo_priority;

COMMIT;
