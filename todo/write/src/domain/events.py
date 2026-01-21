from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from .model import Priority
from typing import Optional

@dataclass(frozen=True)
class TodoCreated:
    id: UUID
    title: str
    description: Optional[str]
    priority: Optional[Priority]
    due_date: Optional[datetime]
    created_at: datetime

    @classmethod
    def from_todo(cls, todo) -> 'TodoCreated':
        return cls(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            priority=todo.priority,
            due_date=todo.due_date,
            created_at=todo.created_at
        )
