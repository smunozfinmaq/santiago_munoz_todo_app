# Implementation Plan: US-002: List Todos

**Branch**: `002-list-todos` | **Date**: 2026-01-22 | **Spec**: [specs/002-list-todos/spec.md](spec.md)
**Input**: Feature specification from `/specs/002-list-todos/spec.md`

## Summary

Implement the "List Todos" functionality on the CQRS Read Side. This service will serve paginated, filtered, and sorted queries from a denormalized read model in the `santiago_munoz_read` schema. The read model is updated by an event consumer (Projection) that listens to events from the Write Side.

## Technical Context

**Language/Version**: Python 3.11+ (AWS Lambda runtime)  
**Primary Dependencies**: `psycopg` (PostgreSQL driver), `aws-lambda-powertools` (Python), `pytest` (testing), `hypothesis` (property-based testing)  
**Storage**: Aurora RDS PostgreSQL (Denormalized read model in `santiago_munoz_read` schema)  
**Testing**: `pytest`, `hypothesis`, local PostgreSQL containers for integration tests  
**Target Platform**: AWS Lambda (serverless)  
**Project Type**: Bounded Context (CQRS Read Side)  
**Performance Goals**: 
- List operations: <200ms (per SC-002 in PRD)
- Handle 100 concurrent read requests
**Constraints**: 
- Explicit SQL (No ORMs)
- Read-only database access for the query API
- Idempotent projection updates
- Soft-deleted items must be filtered out
**Scale/Scope**: 
- Support pagination up to 100 items per page
- Filtering by completion status
- Sorting by creation date or due date

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Requirement | Status |
|------|-------------|--------|
| **C-001** | **Simplicity**: No complex abstractions for SQL queries. | ✅ Pass |
| **C-002** | **Serverless Testability**: Business logic isolated from Lambda runtime. | ✅ Pass |
| **C-003** | **Testing Strategy**: Hypothesis used for pagination/sorting invariants. | ✅ Pass |
| **C-004** | **Persistence**: Read-only repo for Query API; Write/Read repo for Projections. | ✅ Pass |

## Project Structure

### Documentation (this feature)

```text
specs/002-list-todos/
├── plan.md              # This file
├── research.md          # Query optimization and projection consistency
├── data-model.md        # Read-side schema (projections)
├── quickstart.md        # Setup for Read Side testing
├── contracts/           # OpenAPI definitions (GET /todos)
└── tasks.md             # Implementation tasks
```

### Source Code (repository root)

```text
todo/
  read/                   # todo-read deployment unit (Query Side)
    src/
      entrypoints/        
        api.py           # Lambda handler for GET /todos
        consume_events.py # Lambda handler for outbox/SNS events -> Projections
      app/               
        queries.py       # Query logic: sort, filter, paginate
        projections.py   # Event -> State update logic
      infra/
        db.py            # psycopg connection helpers
        repo.py          # SQL Read/Write repositories
    tests/
      unit/
        test_query_logic.py
        test_projection_logic.py
      integration/
        test_read_db_e2e.py
```

**Structure Decision**: The separation into `queries` for serving API requests and `projections` for maintaining state ensures that the API remains fast and simple, while the data is denormalized appropriately.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| CQRS Read Side | High read performance and scalability requirements | Direct reading from write tables would cause contention and coupling. |
