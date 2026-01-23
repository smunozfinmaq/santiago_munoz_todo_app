# Tasks: US-001: Create Todo

## Implementation Strategy
We will follow an incremental approach, starting with the project foundation and then implementing the "Create Todo" user story in two stages: first the essential title-only flow, then adding optional fields and validation. Testing is mandatory per the constitution, so TDD and property-based tests are integrated into each phase.

## Phase 1: Setup
- [X] T001 [P] Initialize repository structure for `todo/write` and `todo/db` in repo root
- [X] T002 [P] Create `todo/write/requirements.txt` with `psycopg`, `aws-lambda-powertools`, and `pydantic`
- [X] T003 [P] Create `todo/write/requirements-dev.txt` with `pytest` and `hypothesis`

## Phase 2: Foundational
- [X] T004 Create Sqitch project in `todo/db` and define separate schemas using `create_read_schema.sql` and `create_write_schema.sql` for CQRS separation
- [X] T005 Implement PostgreSQL connection helper using `psycopg` in `todo/write/src/infra/db.py`
- [X] T006 [P] Implement base `CommandEnvelope` and `Result` shapes in `todo/write/src/app/commands.py`

## Phase 3: [US1] Create Todo (Essential Flow)
**Goal**: Create a todo with only the title and system-generated fields.
**Independent Test**: Use `pytest` to verify a `CreateTodo` command results in a `201 Created` with a UUID and timestamps.

- [X] T007 [P] [US1] Define `Todo` domain entity and `TodoCreated` event in `todo/write/src/domain/model.py` and `todo/write/src/domain/events.py`
- [X] T008 [US1] Write property-based tests for `Todo` creation in `todo/write/tests/unit/test_domain_properties.py`
- [X] T009 [US1] Implement `CreateTodoCommandHandler` logic in `todo/write/src/app/create_todo_command.py`
- [X] T010 [US1] Implement SQL-based `TodoRepository.save()` in `todo/write/src/infra/repo.py`
- [X] T011 [US1] Implement Transactional Outbox insert in `todo/write/src/infra/outbox.py`
- [X] T012 [US1] Create Lambda entrypoint for `POST /todos` in `todo/write/src/entrypoints/api.py`

## Phase 4: [US2] Optional Fields & Validation
**Goal**: Support description, priority, and due_date with full validation.
**Independent Test**: Verify that providing a 501-character title or invalid priority returns a `400 Bad Request`.

- [X] T013 [US1] Update `Todo` model and command handler to support optional fields in `todo/write/src/domain/model.py`
- [X] T014 [US1] Implement input validation logic (max length, enum checks) in `todo/write/src/app/create_todo_command.py`
- [X] T015 [US1] Add property-based tests for validation boundaries in `todo/write/tests/unit/test_command_handlers.py`
- [X] T016 [US1] Update SQL repository to persist optional fields in `todo/write/src/infra/repo.py`

## Phase 5: [US1/2] Idempotency & Persistence
- [X] T017 [US1] Implement command ID check in `todo/write/src/infra/repo.py` using `processed_commands` table
- [X] T018 Integrate idempotency check into the command handler execution flow in `todo/write/src/app/command_handler.py`

## Phase 6: Polish & Integration
- [X] T019 Implement structured logging and X-Ray tracing using Powertools in `todo/write/src/entrypoints/api.py`
- [X] T020 [P] Create `todo/write/tests/integration/test_write_db_e2e.py` for end-to-end flow with a local Postgres container

## Dependencies
- Phase 2 depends on Phase 1
- Phase 3 depends on Phase 2
- Phase 4 depends on Phase 3
- Phase 5 depends on Phase 3
- Phase 6 depends on all previous phases

## Parallel Execution Examples
- T001, T002, T003 can be done in parallel.
- T006 and T007 can be done in parallel once T001 is finished.
- T020 can be prepared while Phase 3/4 implementation is in progress.
