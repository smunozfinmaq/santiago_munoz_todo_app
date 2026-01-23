# Tasks: US-002: List Todos

## Implementation Strategy
We will implement the List Todos feature using a CQRS Read Side approach. First, we will set up the Read Side project structure and dependencies. Then, we will define the read model schema and the projection logic to keep it updated from domain events. Finally, we will implement the query API with pagination, filtering, and sorting, backed by property-based tests.

## Phase 1: Setup & Foundational
- [X] T001 Initialize repository structure for `todo/read` and metadata in `todo/read/requirements.txt`
- [X] T002 Update `todo/db` with Sqitch migration for `todo_read_model` and `processed_events`
- [X] T003 [P] Implement Read Side PostgreSQL connection helper in `todo/read/src/infra/db.py`

## Phase 2: Projections (Sync Write to Read)
- [X] T004 Define event consumption shape and `TodoProjection` logic in `todo/read/src/app/projections.py`
- [X] T005 Implement `TodoReadRepository.upsert()` for the projection in `todo/read/src/infra/repo.py`
- [X] T006 [P] Create Lambda handler for event consumption (Projection) in `todo/read/src/entrypoints/consume_events.py`

## Phase 3: Query Implementation (GET /todos)
- [X] T007 Define `QueryEnvelope` and `PaginatedResponse` in `todo/read/src/app/queries.py`
- [X] T008 [P] Implement dynamic SQL query builder for filtering and sorting in `todo/read/src/infra/repo.py`
- [X] T009 Write property-based tests for pagination and sorting logic in `todo/read/tests/unit/test_query_logic.py`
- [X] T010 [P] Implement `ListTodosQueryHandler` in `todo/read/src/app/queries.py`
- [X] T011 Create Lambda entrypoint for `GET /todos` in `todo/read/src/entrypoints/api.py`

## Phase 4: Verification & Polish
- [X] T012 Implement input validation for query parameters (page, limit, sort) using Pydantic
- [X] T013 [P] Create `todo/read/tests/integration/test_read_db_e2e.py` for full query flow
- [X] T014 Add structured logging and metrics to the Read Side Lambda handlers

## Dependencies
- Phase 2 depends on Phase 1
- Phase 3 depends on Phase 1
- Phase 4 depends on Phase 2 and 3

## Parallel Execution Examples
- T003 and T005 can be started in parallel once Phase 1 setup is done.
- T009 (Tests) can be written while T008 (Implementation) is in progress.
