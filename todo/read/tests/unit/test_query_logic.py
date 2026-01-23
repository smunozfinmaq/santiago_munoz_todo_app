from hypothesis import given, strategies as st
from todo.read.src.app.queries import ListTodosQueryHandler, ListTodosQuery
import pytest
from unittest.mock import MagicMock
import math

@given(
    page=st.integers(min_value=1, max_value=100),
    limit=st.integers(min_value=1, max_value=100),
    status=st.one_of(st.none(), st.sampled_from(["completed", "pending"])),
    sort=st.sampled_from(["created_at", "due_date"]),
    order=st.sampled_from(["asc", "desc"])
)
def test_query_handler_metadata_logic(page, limit, status, sort, order):
    """
    Property-based test to ensure pagination metadata is calculated correctly
    and repository is called with the right parameters.
    """
    mock_repo = MagicMock()
    total_count = 250
    mock_repo.list_todos.return_value = {
        "items": [], 
        "total_count": total_count
    }
    
    handler = ListTodosQueryHandler(repo=mock_repo)
    query = ListTodosQuery(page=page, limit=limit, status=status, sort=sort, order=order)
    
    response = handler.handle(query)
    
    assert response.metadata.page == page
    assert response.metadata.limit == limit
    assert response.metadata.total_count == total_count
    assert response.metadata.total_pages == math.ceil(total_count / limit)
    
    # Verify repo received the correct arguments
    mock_repo.list_todos.assert_called_with(
        page=page,
        limit=limit,
        status=status,
        sort_by=sort,
        order=order
    )

def test_query_validation_errors():
    """
    Ensures Pydantic validation works as expected.
    """
    with pytest.raises(ValueError):
        ListTodosQuery(page=0) # Must be >= 1

    with pytest.raises(ValueError):
        ListTodosQuery(limit=101) # Max 100
