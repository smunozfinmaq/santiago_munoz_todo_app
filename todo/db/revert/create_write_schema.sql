BEGIN;

DROP TABLE santiago_munoz_write.outbox;
DROP TABLE santiago_munoz_write.processed_commands;
DROP TABLE santiago_munoz_write.todos;
DROP TYPE santiago_munoz_write.todo_priority;
DROP SCHEMA santiago_munoz_write;

COMMIT;
