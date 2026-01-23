import json
from uuid import UUID
from typing import Optional, Dict, Any
from ..domain.model import Todo
from ..domain.events import TodoCreated
from .db import get_db_transaction

class AlreadyProcessedError(Exception):
    def __init__(self, status_code: int, body: Dict[str, Any]):
        self.status_code = status_code
        self.body = body

class TodoRepository:
    def save(self, todo: Todo, event: TodoCreated, command_id: UUID) -> None:
        with get_db_transaction() as cur:
            # 1. Idempotency Check
            cur.execute(
                "SELECT result_status, result_body FROM santiago_munoz_processed_commands WHERE command_id = %s",
                (command_id,)
            )
            existing = cur.fetchone()
            if existing:
                raise AlreadyProcessedError(
                    status_code=existing["result_status"],
                    body=existing["result_body"]
                )

            # 2. Insert Todo
            cur.execute(
                """
                INSERT INTO santiago_munoz_todos (id, title, description, priority, due_date, is_completed, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    todo.id, todo.title, todo.description, 
                    todo.priority.value if todo.priority else None, 
                    todo.due_date, todo.is_completed, todo.created_at, todo.updated_at
                )
            )

            # 3. Insert Outbox Event
            event_payload = {
                "id": str(event.id),
                "title": event.title,
                "description": event.description,
                "priority": event.priority.value if event.priority else None,
                "due_date": event.due_date.isoformat() if event.due_date else None,
                "created_at": event.created_at.isoformat()
            }
            cur.execute(
                """
                INSERT INTO santiago_munoz_outbox (aggregate_id, event_type, payload)
                VALUES (%s, %s, %s)
                """,
                (todo.id, "TodoCreated", json.dumps(event_payload))
            )

            # 4. Record Command
            result_body = {
                "id": str(todo.id),
                "title": todo.title,
                "description": todo.description,
                "priority": todo.priority.value if todo.priority else None,
                "due_date": todo.due_date.isoformat() if todo.due_date else None,
                "is_completed": todo.is_completed,
                "created_at": todo.created_at.isoformat(),
                "updated_at": todo.updated_at.isoformat()
            }
            cur.execute(
                "INSERT INTO santiago_munoz_processed_commands (command_id, result_status, result_body) VALUES (%s, %s, %s)",
                (command_id, 201, json.dumps(result_body))
            )
