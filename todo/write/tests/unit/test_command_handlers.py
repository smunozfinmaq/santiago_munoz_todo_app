from hypothesis import given, strategies as st
from todo.write.src.app.create_todo_command import CreateTodoCommandHandler
from todo.write.src.app.commands import CommandEnvelope
import pytest
from unittest.mock import MagicMock
from uuid import uuid4

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def handler(mock_repo):
    return CreateTodoCommandHandler(repo=mock_repo)

@given(
    title=st.text(min_size=1, max_size=500),
    description=st.one_of(st.none(), st.text(max_size=500)),
    priority=st.sampled_from(["Low", "Medium", "High", None]),
    due_date=st.one_of(st.none(), st.datetimes().map(lambda d: d.isoformat()))
)
def test_handler_valid_inputs(title, description, priority, due_date):
    mock_repo = MagicMock()
    handler = CreateTodoCommandHandler(repo=mock_repo)
    command_id = uuid4()
    payload = {
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date
    }
    envelope = CommandEnvelope(command_id=command_id, payload=payload)
    
    result = handler.handle(envelope)
    
    if title.strip():
        assert result.status_code == 201
        assert mock_repo.save.called
    else:
        assert result.status_code == 400
        assert "Title is required" in result.error

def test_handler_invalid_priority(handler):
    envelope = CommandEnvelope(
        command_id=uuid4(), 
        payload={"title": "Task", "priority": "Urgent"}
    )
    result = handler.handle(envelope)
    assert result.status_code == 400
    assert "Invalid priority" in result.error

def test_handler_invalid_date(handler):
    envelope = CommandEnvelope(
        command_id=uuid4(), 
        payload={"title": "Task", "due_date": "not-a-date"}
    )
    result = handler.handle(envelope)
    assert result.status_code == 400
    assert "due_date must be a valid ISO-8601 string" in result.error
