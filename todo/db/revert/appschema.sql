BEGIN;

DROP TABLE santiago_munoz_outbox;
DROP TABLE santiago_munoz_processed_commands;
DROP TABLE santiago_munoz_todos;
DROP TYPE santiago_munoz_todo_priority;

COMMIT;
