import json
from aws_lambda_powertools import Logger
from ..app.projections import TodoProjectionHandler
from ..infra.repo import TodoReadRepository

logger = Logger()

def lambda_handler(event, context):
    """
    Consumer for outbox events (simulated via manual trigger or SNS/EventBridge).
    Processes events to update the read side projections.
    """
    repo = TodoReadRepository()
    handler = TodoProjectionHandler(repo)
    
    try:
        # Expected format: {'event_id': '...', 'event_type': '...', 'payload': {...}}
        event_id = event['event_id']
        event_type = event['event_type']
        payload = event['payload']
        
        logger.info(f"Processing event {event_id} of type {event_type}")
        handler.handle(event_id, event_type, payload)
        
        return {"status": "success"}
    except Exception as e:
        logger.exception("Failed to project event")
        raise e
