from hypothesis import given, strategies as st
from todo.write.src.domain.model import Todo, Priority
import pytest
from uuid import UUID
from datetime import datetime

@given(
    title=st.text(min_size=1, max_size=500).map(lambda s: s.strip()).filter(lambda s: len(s) > 0),
    description=st.one_of(st.none(), st.text(max_size=500)),
    priority=st.one_of(st.none(), st.sampled_from(Priority)),
    due_date=st.one_of(st.none(), st.datetimes())
)
def test_todo_creation_valid_properties(title, description, priority, due_date):
    todo = Todo.create(
        title=title,
        description=description,
        priority=priority,
        due_date=due_date
    )
    
    assert isinstance(todo.id, UUID)
    assert todo.title == title
    assert todo.description == (description.strip() if description else None)
    assert todo.priority == priority
    assert todo.due_date == due_date
    assert todo.is_completed is False
    assert isinstance(todo.created_at, datetime)
    assert todo.created_at == todo.updated_at

@given(st.text(min_size=501))
def test_todo_creation_invalid_title_length(long_title):
    with pytest.raises(ValueError, match="Title must be 500 characters or less"):
        Todo.create(title=long_title)

@given(st.text().filter(lambda s: not s.strip()))
def test_todo_creation_empty_title(empty_title):
    with pytest.raises(ValueError, match="Title is required"):
        Todo.create(title=empty_title)

@given(st.text(min_size=501))
def test_todo_creation_invalid_description_length(long_desc):
    with pytest.raises(ValueError, match="Description must be 500 characters or less"):
        Todo.create(title="Valid Title", description=long_desc)
