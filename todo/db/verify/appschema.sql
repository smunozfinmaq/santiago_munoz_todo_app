BEGIN;

SELECT id, title, description, priority, due_date, is_completed, created_at, updated_at FROM santiago_munoz_todos WHERE FALSE;
SELECT command_id, result_status, result_body, processed_at FROM santiago_munoz_processed_commands WHERE FALSE;
SELECT id, aggregate_id, event_type, payload, created_at, published_at FROM santiago_munoz_outbox WHERE FALSE;

ROLLBACK;
