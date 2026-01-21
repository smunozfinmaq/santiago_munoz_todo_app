import os
import pytest
import json
from uuid import uuid4
from todo.write.src.entrypoints.api import lambda_handler

@pytest.fixture(scope="function")
def setup_database(postgresql):
    """
    Sets up the temporary PostgreSQL database with the required schema.
    """
    host = postgresql.info.host
    port = postgresql.info.port
    user = postgresql.info.user
    dbname = postgresql.info.dbname
    
    # We use a passwordless connection for the local fixture
    db_url = f"postgresql://{user}@{host}:{port}/{dbname}"
    os.environ["DATABASE_URL"] = db_url

    # Run the deployment script
    deploy_script = os.path.abspath(os.path.join(os.getcwd(), "todo/db/deploy/appschema.sql"))
    with open(deploy_script, 'r') as f:
        sql = f.read()
        with postgresql.cursor() as cur:
            cur.execute(sql)
    
    return postgresql

def test_create_todo_e2e_flow(setup_database):
    """
    Tests the complete flow from Lambda entrypoint to DB persistence and idempotency.
    """
    db = setup_database
    command_id = str(uuid4())
    
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
    
    response = lambda_handler(event, None)
    
    assert response["statusCode"] == 201
    body = json.loads(response["body"])
    assert body["title"] == "Integration Test Task"
    assert "id" in body
    
    # 2. Verify Database State
    with db.cursor() as cur:
        # Check Todo table
        cur.execute("SELECT title, priority, description FROM todos WHERE id = %s", (body["id"],))
        row = cur.fetchone()
        assert row is not None
        assert row[0] == "Integration Test Task"
        assert row[1] == "High"
        assert row[2] == "Testing the full write stack"
        
        # Check Outbox table
        cur.execute("SELECT event_type FROM outbox WHERE aggregate_id = %s", (body["id"],))
        assert cur.fetchone()[0] == "TodoCreated"
        
        # Check Idempotency table
        cur.execute("SELECT result_status FROM processed_commands WHERE command_id = %s", (command_id,))
        assert cur.fetchone()[0] == 201

    # 3. Test Idempotency (Retry with same Command ID)
    response_retry = lambda_handler(event, None)
    assert response_retry["statusCode"] == 201
    body_retry = json.loads(response_retry["body"])
    assert body_retry["id"] == body["id"]
    
    # Verify no duplicate was created
    with db.cursor() as cur:
        cur.execute("SELECT count(*) FROM todos WHERE title = %s", ("Integration Test Task",))
        assert cur.fetchone()[0] == 1

def test_create_todo_validation_error(setup_database):
    """
    Tests that validation errors result in no DB changes.
    """
    db = setup_database
    event = {
        "body": json.dumps({
            "title": "" # Invalid: empty title
        }),
        "headers": {
            "X-Command-ID": str(uuid4())
        }
    }
    
    response = lambda_handler(event, None)
    assert response["statusCode"] == 400
    assert "Title is required" in json.loads(response["body"])["error"]
    
    with db.cursor() as cur:
        cur.execute("SELECT count(*) FROM todos")
        assert cur.fetchone()[0] == 0
