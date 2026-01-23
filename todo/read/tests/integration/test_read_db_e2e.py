import pytest
import json
from uuid import uuid4
from unittest.mock import MagicMock
from datetime import datetime
from todo.write.src.entrypoints.api import lambda_handler as write_handler
from todo.read.src.entrypoints.api import lambda_handler as query_handler

@pytest.fixture(scope="function")
def mock_context():
    context = MagicMock()
    context.function_name = "test_func"
    context.memory_limit_in_mb = 128
    context.invoked_function_arn = "arn:test"
    context.aws_request_id = "request_id"
    return context

@pytest.fixture(scope="function")
def mock_db(mocker):
    """
    Mocks the database transaction and connection for read side integration testing.
    """
    mock_cursor = MagicMock()
    
    # Patch where they are USED in the repository
    mocker.patch("todo.read.src.infra.repo.get_db_cursor", return_value=MagicMock(__enter__=lambda s: mock_cursor))
    mocker.patch("todo.read.src.infra.repo.get_db_transaction", return_value=MagicMock(__enter__=lambda s: mock_cursor))
    
    return mock_cursor

def test_read_side_list_flow(mock_db, mock_context):
    """
    Tests the list query flow using mocks.
    """
    todo_id = str(uuid4())
    now = datetime.now()
    
    # Configure mock for query side
    mock_db.fetchall.return_value = [
        {
            "id": todo_id,
            "title": "Mocked Todo",
            "description": "Visible in list",
            "priority": "Medium",
            "due_date": None,
            "is_completed": False,
            "created_at": now,
            "updated_at": now
        }
    ]
    mock_db.fetchone.return_value = {"total": 1}
    
    query_event = {
        "queryStringParameters": {
            "status": "pending",
            "page": "1",
            "limit": "10"
        }
    }
    
    response = query_handler(query_event, mock_context)
    
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    
    assert body["metadata"]["total_count"] == 1
    assert body["items"][0]["id"] == todo_id
    assert body["items"][0]["title"] == "Mocked Todo"
    
    # Verify the query was correct
    assert "FROM santiago_munoz_todos" in mock_db.execute.call_args_list[0][0][0]
    assert "WHERE is_completed = %s" in mock_db.execute.call_args_list[0][0][0]

def test_read_side_empty_list(mock_db, mock_context):
    """
    Tests the case where no todos are found.
    """
    mock_db.fetchall.return_value = []
    mock_db.fetchone.return_value = {"total": 0}
    
    response = query_handler({"queryStringParameters": {}}, mock_context)
    
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert len(body["items"]) == 0
    assert body["metadata"]["total_count"] == 0
