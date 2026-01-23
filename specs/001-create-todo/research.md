# Research: US-001: Create Todo

## Domain Analysis: Idempotency & Transactions

### Decision: Client-Side Command IDs
- **Problem**: In a serverless/distributed environment, a client might retry a `POST /todos` request if they don't receive a response (e.g., due to a timeout), leading to duplicate todos.
- **Solution**: The API will require a `X-Command-ID` header (UUID) for any state-changing operation.
- **Implementation**: 
  - Save the `command_id` in a dedicated `santiago_munoz_processed_commands` table.
  - Wrap the check-and-insert in a single PostgreSQL transaction.
- **Rationale**: Provides absolute guarantees against double-creation without complex distributed locks.

### Decision: Transactional Outbox Pattern
- **Problem**: We need to update the read models (Read Side) whenever a todo is created (Write Side). Sending an event to SNS/EventBridge *after* the DB commit can fail, leading to inconsistency.
- **Solution**: Insert the event into an `outbox` table within the *same* database transaction that creates the todo. A separate (or triggered) process will poll the outbox and publish to SNS.
- **Rationale**: Ensures "at-least-once" delivery of events.

## Technology Best Practices

### psycopg 3 (vs psycopg2)
- **Decision**: Use `psycopg` (v3).
- **Rationale**: Better support for Python type hinting, optimized binary transfers, and improved connection pooling suitable for serverless bursts.
- **Pattern**: Use `Connection.execute()` for simple queries and context managers for transactions.

### Domain Modeling without Infrastructure
- **Decision**: Define the `Todo` aggregate in `domain/model.py` using pure Python / dataclasses.
- **Rationale**: Complies with the Constitution (Serverless testability). Logic can be tested 100% locally with `pytest` and `hypothesis`.

## Integration Research

### AWS Lambda Powertools
- **Decision**: Use for Structured Logging, Metrics, and Tracer (X-Ray).
- **Rationale**: Standardizes observability and simplifies handler boilerplate.

### Local Integration Testing
- **Decision**: Use `pytest-postgresql` or Docker containers for integration tests.
- **Rationale**: Facilitates local verification of raw SQL queries without depending on a live Aurora instance.
