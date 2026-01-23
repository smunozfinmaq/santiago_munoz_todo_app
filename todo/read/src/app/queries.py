from pydantic import BaseModel, Field
from typing import List, Optional, Any
import math

class TodoReadModel(BaseModel):
    """
    Schema for a single Todo item in the read model.
    """
    id: str
    title: str
    description: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None
    is_completed: bool
    created_at: str
    updated_at: str

class PaginationMetadata(BaseModel):
    """
    Standard metadata for paginated responses.
    """
    total_count: int
    page: int
    limit: int
    total_pages: int

    @classmethod
    def create(cls, total_count: int, page: int, limit: int) -> 'PaginationMetadata':
        total_pages = math.ceil(total_count / limit) if total_count > 0 else 0
        return cls(
            total_count=total_count,
            page=page,
            limit=limit,
            total_pages=total_pages
        )

class PaginatedResponse(BaseModel):
    """
    A full paginated response with items and metadata.
    """
    items: List[TodoReadModel]
    metadata: PaginationMetadata

class ListTodosQuery(BaseModel):
    """
    Validated query parameters for listing todos.
    """
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)
    status: Optional[str] = None # 'completed' or 'pending'
    sort: str = Field(default="created_at")
    order: str = Field(default="desc")

class ListTodosQueryHandler:
    def __init__(self, repo):
        self.repo = repo

    def handle(self, query: ListTodosQuery) -> PaginatedResponse:
        """
        Executes the list query and formats the response.
        """
        result = self.repo.list_todos(
            page=query.page,
            limit=query.limit,
            status=query.status,
            sort_by=query.sort,
            order=query.order
        )
        
        items = []
        for row in result["items"]:
            items.append(
                TodoReadModel(
                    id=str(row["id"]),
                    title=row["title"],
                    description=row["description"],
                    priority=row["priority"],
                    due_date=row["due_date"].isoformat() if row["due_date"] else None,
                    is_completed=row["is_completed"],
                    created_at=row["created_at"].isoformat(),
                    updated_at=row["updated_at"].isoformat()
                )
            )
        
        metadata = PaginationMetadata.create(
            total_count=result["total_count"],
            page=query.page,
            limit=query.limit
        )
        
        return PaginatedResponse(items=items, metadata=metadata)
