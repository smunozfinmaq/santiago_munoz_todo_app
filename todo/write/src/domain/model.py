from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4
from enum import Enum
from typing import Optional

class Priority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

@dataclass(frozen=True)
class Todo:
    id: UUID
    title: str
    description: Optional[str] = None
    priority: Optional[Priority] = None
    due_date: Optional[datetime] = None
    is_completed: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def create(cls, title: str, description: Optional[str] = None, 
               priority: Optional[Priority] = None, 
               due_date: Optional[datetime] = None) -> 'Todo':
        if not title or not title.strip():
            raise ValueError("Title is required")
        if len(title) > 500:
            raise ValueError("Title must be 500 characters or less")
        if description and len(description) > 500:
             raise ValueError("Description must be 500 characters or less")
        
        now = datetime.now(timezone.utc)
        return cls(
            id=uuid4(),
            title=title.strip(),
            description=description.strip() if description else None,
            priority=priority,
            due_date=due_date,
            is_completed=False,
            created_at=now,
            updated_at=now
        )
