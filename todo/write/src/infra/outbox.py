from .db import get_db_transaction
from typing import List

class OutboxPublisher:
    """
    Handles marking outbox events as published.
    """
    def mark_as_published(self, event_ids: List[int]) -> None:
        with get_db_transaction() as cur:
            cur.execute(
                "UPDATE outbox SET published_at = NOW() WHERE id = ANY(%s)",
                (event_ids,)
            )

    def get_pending_events(self, limit: int = 100):
        with get_db_transaction() as cur:
            cur.execute(
                "SELECT id, aggregate_id, event_type, payload FROM outbox WHERE published_at IS NULL LIMIT %s",
                (limit,)
            )
            return cur.fetchall()
