import json
from uuid import UUID
from aws_lambda_powertools import Logger, Tracer
from ..app.commands import CommandEnvelope
from ..app.create_todo_command import CreateTodoCommandHandler
from ..infra.repo import TodoRepository

logger = Logger()
tracer = Tracer()

# Singleton-like instantiation for warmed-up performance
repo = TodoRepository()
handler = CreateTodoCommandHandler(repo)

@tracer.capture_lambda_handler
@logger.inject_lambda_context
def lambda_handler(event: dict, context) -> dict:
    """
    AWS Lambda entrypoint for creating a Todo.
    """
    try:
        # 1. Parse Input
        body = json.loads(event.get("body", "{}"))
        headers = {k.lower(): v for k, v in event.get("headers", {}).items()}
        command_id_str = headers.get("x-command-id")
        
        if not command_id_str:
            return _response(400, {"error": "Missing X-Command-ID header"})
        
        try:
            command_id = UUID(command_id_str)
        except ValueError:
            return _response(400, {"error": "Invalid X-Command-ID format. Must be a UUID"})

        # 2. Execute Command
        envelope = CommandEnvelope(
            command_id=command_id,
            payload=body
        )
        
        result = handler.handle(envelope)
        
        # 3. Return Response
        return _response(
            result.status_code, 
            result.body if result.status_code < 400 else {"error": result.error}
        )

    except json.JSONDecodeError:
        return _response(400, {"error": "Invalid JSON body"})
    except Exception as e:
        logger.exception("Failed to process create todo request")
        return _response(500, {"error": "Internal server error"})

def _response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }
