from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict, Any
from .db import get_db_transaction, get_db_cursor

class TodoReadRepository:
    def upsert(
        self, 
        todo_id: UUID, 
        title: str, 
        description: Optional[str], 
        priority: Optional[str], 
        due_date: Optional[datetime], 
        is_completed: bool, 
        created_at: datetime, 
        updated_at: datetime,
        event_id: UUID
    ) -> None:
        """
        Idempotently updates the read model from an event.
        """
        with get_db_transaction() as cur:
            # 1. Idempotency check for the event
            cur.execute("SELECT 1 FROM santiago_munoz_read.processed_events WHERE event_id = %s", (event_id,))
            if cur.fetchone():
                return

            # 2. Upsert into read model
            cur.execute(
                """
                INSERT INTO santiago_munoz_read.todos (id, title, description, priority, due_date, is_completed, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    title = EXCLUDED.title,
                    description = EXCLUDED.description,
                    priority = EXCLUDED.priority,
                    due_date = EXCLUDED.due_date,
                    is_completed = EXCLUDED.is_completed,
                    updated_at = EXCLUDED.updated_at
                """,
                (todo_id, title, description, priority, due_date, is_completed, created_at, updated_at)
            )

            # 3. Mark event as processed
            cur.execute("INSERT INTO santiago_munoz_read.processed_events (event_id) VALUES (%s)", (event_id,))

    def list_todos(
        self, 
        page: int = 1, 
        limit: int = 10, 
        status: Optional[str] = None, 
        sort_by: str = "created_at", 
        order: str = "desc"
    ) -> Dict[str, Any]:
        """
        Query side: Lists todos with pagination, filtering, and sorting.
        """
        offset = (page - 1) * limit
        
        # Base queries
        where_clause = ""
        params = []
        
        if status:
            is_completed = (status == "completed")
            where_clause = "WHERE is_completed = %s"
            params.append(is_completed)
        
        # Validate sort field
        allowed_sort = ["created_at", "due_date"]
        if sort_by not in allowed_sort:
            sort_by = "created_at"
        
        allowed_order = ["asc", "desc"]
        if order.lower() not in allowed_order:
            order = "desc"

        query = f"""
            SELECT id, title, description, priority, due_date, is_completed, created_at, updated_at
            FROM santiago_munoz_read.todos
            {where_clause}
            ORDER BY {sort_by} {order}, id ASC
            LIMIT %s OFFSET %s
        """
        
        count_query = f"SELECT COUNT(*) as total FROM santiago_munoz_read.todos {where_clause}"
        
        with get_db_cursor() as cur:
            cur.execute(query, tuple(params + [limit, offset]))
            items = cur.fetchall()
            
            cur.execute(count_query, tuple(params))
            total_count = cur.fetchone()["total"]
            
        return {
            "items": items,
            "total_count": total_count
        }
