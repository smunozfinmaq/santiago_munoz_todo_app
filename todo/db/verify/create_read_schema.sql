BEGIN;

SELECT id, title, description, priority, due_date, is_completed, created_at, updated_at FROM santiago_munoz_read.todos WHERE FALSE;
SELECT event_id, processed_at FROM santiago_munoz_read.processed_events WHERE FALSE;

ROLLBACK;
