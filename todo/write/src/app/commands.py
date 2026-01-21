from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, Any
from uuid import UUID

T = TypeVar('T')

class CommandEnvelope(BaseModel, Generic[T]):
    command_id: UUID
    payload: T

class CommandResult(BaseModel):
    status_code: int
    body: Optional[Any] = None
    error: Optional[str] = None

    @classmethod
    def success(cls, body: Any = None, status_code: int = 200) -> 'CommandResult':
        return cls(status_code=status_code, body=body)

    @classmethod
    def failure(cls, error: str, status_code: int = 400) -> 'CommandResult':
        return cls(status_code=status_code, error=error)
