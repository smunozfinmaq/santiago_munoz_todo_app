from typing import Optional, Dict, Any
from datetime import datetime
from .commands import CommandEnvelope, CommandResult
from ..domain.model import Todo, Priority
from ..domain.events import TodoCreated
from ..infra.repo import AlreadyProcessedError

class CreateTodoCommandHandler:
    def __init__(self, repo):
        self.repo = repo

    def handle(self, envelope: CommandEnvelope[Dict[str, Any]]) -> CommandResult:
        try:
            payload = envelope.payload
            
            # Map string priority to Enum if provided
            priority = None
            if payload.get("priority"):
                try:
                    priority = Priority(payload["priority"])
                except ValueError:
                    return CommandResult.failure(
                        error=f"Invalid priority: {payload['priority']}. Must be one of Low, Medium, High", 
                        status_code=400
                    )
            
            # Handle due_date string to datetime
            due_date = payload.get("due_date")
            if isinstance(due_date, str):
                try:
                    due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                except ValueError:
                    return CommandResult.failure(
                        error="due_date must be a valid ISO-8601 string", 
                        status_code=400
                    )

            todo = Todo.create(
                title=payload.get("title"),
                description=payload.get("description"),
                priority=priority,
                due_date=due_date
            )
            
            event = TodoCreated.from_todo(todo)
            
            # The repo will handle the transaction (idempotency, todo, outbox)
            try:
                self.repo.save(todo, event, envelope.command_id)
            except AlreadyProcessedError as e:
                return CommandResult.success(body=e.body, status_code=e.status_code)
            
            return CommandResult.success(
                body={
                    "id": str(todo.id),
                    "title": todo.title,
                    "description": todo.description,
                    "priority": todo.priority.value if todo.priority else None,
                    "due_date": todo.due_date.isoformat().replace('+00:00', 'Z') if todo.due_date else None,
                    "is_completed": todo.is_completed,
                    "created_at": todo.created_at.isoformat().replace('+00:00', 'Z'),
                    "updated_at": todo.updated_at.isoformat().replace('+00:00', 'Z')
                },
                status_code=201
            )
        except ValueError as e:
            return CommandResult.failure(error=str(e), status_code=400)
        except Exception as e:
            # In a real app, we'd log this exception
            return CommandResult.failure(error=f"Unexpected error: {str(e)}", status_code=500)
