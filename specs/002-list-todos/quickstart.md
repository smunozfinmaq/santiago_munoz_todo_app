# Quickstart: US-002: List Todos

## Local Development Setup

1. **Install Dependencies**:
   Ensure you have the development environment ready.
   ```bash
   cd todo/read
   uv pip install -r requirements.txt -r requirements-dev.txt
   ```

2. **Database Setup**:
   The read models need to be initialized. For local testing, use a PostgreSQL container.
   ```bash
   # Run the read schema deployment script located in todo/db/deploy/read_model.sql (to be created)
   ```

3. **Running Tests**:
   - **Unit Tests**: Focus on the query builder and pagination logic.
     ```bash
     $env:PYTHONPATH = "."
     pytest tests/unit/test_query_logic.py
     ```
   - **Integration Tests**: Verify end-to-end flow with a real database.
     ```bash
     pytest tests/integration/test_read_db_e2e.py
     ```

## Implementation Workflow

1.  **Phase 0**: Research query optimization (denormalization vs directly reading write tables).
2.  **Phase 1**: Define the `todo_read_model` schema and Projection logic.
3.  **Phase 2**: Implement the `TodoQueryService` with TDD (using `hypothesis` for pagination).
4.  **Phase 3**: Implement the Event Consumer (Projection) to keep the read model synced.
5.  **Phase 4**: Create the Lambda entrypoint for `GET /todos`.
6.  **Phase 5**: Verify with E2E integration tests.
