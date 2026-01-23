import pytest
import json
from uuid import uuid4
from unittest.mock import MagicMock, patch
from todo.write.src.entrypoints.api import lambda_handler

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
    Mocks the database transaction and connection for integration testing 
    without a real PostgreSQL instance.
    """
    # Create the mock cursor and connection
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    
    # Patch where they are USED in the repository
    mocker.patch("todo.write.src.infra.repo.get_db_transaction", return_value=MagicMock(__enter__=lambda s: mock_cursor))
    
    return mock_cursor

def test_create_todo_e2e_flow(mock_db, mock_context):
    """
    Tests the complete flow using mocks to simulate DB behavior.
    """
    command_id = str(uuid4())
    
    # Configure mock for idempotency check (not found)
    mock_db.fetchone.side_effect = [
        None, # First check: result_status from processed_commands
    ]
    
    # 1. Initial Creation
    event = {
        "body": json.dumps({
            "title": "Integration Test Task",
            "description": "Testing the full write stack",
            "priority": "High",
            "due_date": "2026-12-31T23:59:59Z"
        }),
        "headers": {
            "X-Command-ID": command_id
        }
    }
    
    response = lambda_handler(event, mock_context)
    
    assert response["statusCode"] == 201
    body = json.loads(response["body"])
    assert body["title"] == "Integration Test Task"
    assert "id" in body
    
    # 2. Verify Database Calls
    # Check if idempotency was checked
    assert "SELECT result_status, result_body FROM santiago_munoz_write.processed_commands" in mock_db.execute.call_args_list[0][0][0]
    
    # Check if Todo was inserted
    assert "INSERT INTO santiago_munoz_write.todos" in mock_db.execute.call_args_list[1][0][0]
    
    # Check if Outbox was inserted
    assert "INSERT INTO santiago_munoz_write.outbox" in mock_db.execute.call_args_list[2][0][0]
    
    # Check if Command was recorded
    assert "INSERT INTO santiago_munoz_write.processed_commands" in mock_db.execute.call_args_list[3][0][0]

def test_create_todo_idempotency_flow(mock_db, mock_context):
    """
    Tests that if a command was already processed, it returns the cached result.
    """
    command_id = str(uuid4())
    todo_id = str(uuid4())
    
    # Configure mock for idempotency check (found)
    mock_db.fetchone.return_value = {
        "result_status": 201,
        "result_body": {"id": todo_id, "title": "Already Exists"}
    }
    
    event = {
        "body": json.dumps({"title": "Doesn't matter"}),
        "headers": {"X-Command-ID": command_id}
    }
    
    response = lambda_handler(event, mock_context)
    
    assert response["statusCode"] == 201
    body = json.loads(response["body"])
    assert body["id"] == todo_id
    assert body["title"] == "Already Exists"
    
    # Verify only the select was called, no inserts
    assert mock_db.execute.call_count == 1
    assert "SELECT" in mock_db.execute.call_args[0][0]

def test_create_todo_validation_error(mock_db, mock_context):
    """
    Tests that validation errors return 400 and don't touch the DB.
    """
    event = {
        "body": json.dumps({"title": ""}), # Invalid
        "headers": {"X-Command-ID": str(uuid4())}
    }
    
    response = lambda_handler(event, mock_context)
    assert response["statusCode"] == 400
    assert mock_db.execute.call_count == 0
