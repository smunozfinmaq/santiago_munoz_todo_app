from typing import Dict, Any
from uuid import UUID
from datetime import datetime
from ..infra.repo import TodoReadRepository

class TodoProjectionHandler:
    def __init__(self, repo: TodoReadRepository):
        self.repo = repo

    def handle(self, event_id: str, event_type: str, payload: Dict[str, Any]) -> None:
        """
        Dispatches the event to the appropriate projection logic.
        """
        if event_type == "TodoCreated":
            self._project_todo_created(event_id, payload)
        # Add cases for updated/deleted here in the future
    
    def _project_todo_created(self, event_id: str, payload: Dict[str, Any]) -> None:
        """
        Maps TodoCreated event to the read model.
        """
        # Parsing dates from ISO strings in the event payload
        created_at = datetime.fromisoformat(payload["created_at"])
        due_date = datetime.fromisoformat(payload["due_date"]) if payload.get("due_date") else None
        
        self.repo.upsert(
            todo_id=UUID(payload["id"]),
            title=payload["title"],
            description=payload.get("description"),
            priority=payload.get("priority"),
            due_date=due_date,
            is_completed=False,
            created_at=created_at,
            updated_at=created_at,
            event_id=UUID(event_id)
        )
