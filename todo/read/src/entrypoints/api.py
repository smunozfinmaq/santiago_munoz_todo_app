import json
from aws_lambda_powertools import Logger, Tracer
from ..app.queries import ListTodosQuery, ListTodosQueryHandler
from ..infra.repo import TodoReadRepository

logger = Logger()
tracer = Tracer()

repo = TodoReadRepository()
handler = ListTodosQueryHandler(repo)

@tracer.capture_lambda_handler
@logger.inject_lambda_context
def lambda_handler(event: dict, context) -> dict:
    """
    AWS Lambda entrypoint for listing todos.
    Supports pagination, filtering, and sorting.
    """
    try:
        # 1. Parse Input
        params = event.get("queryStringParameters") or {}
        
        # 2. Validate and Execute Query
        try:
            # Pydantic will auto-convert string params to int/bool as needed
            query = ListTodosQuery(**params)
        except Exception as e:
            return _response(400, {"error": str(e)})
            
        result = handler.handle(query)
        
        # 3. Return Response
        return _response(200, result.model_dump())

    except Exception as e:
        logger.exception("Failed to process list todos request")
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
