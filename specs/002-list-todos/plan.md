# Implementation Plan: US-002: List Todos

**Branch**: `002-list-todos` | **Date**: 2026-01-22 | **Spec**: [specs/002-list-todos/spec.md](spec.md)
**Input**: Feature specification from `/specs/002-list-todos/spec.md`

## Summary

Implement the "List Todos" functionality by querying the shared database table directly. This simplified architecture removes the need for denormalized read models and event-driven projections, while still providing paginated, filtered, and sorted results. All tables use the `santiago_munoz_` prefix.

## Technical Context

**Language/Version**: Python 3.11+ (AWS Lambda runtime)  
**Primary Dependencies**: `psycopg` (PostgreSQL driver), `aws-lambda-powertools` (Python), `pytest` (testing), `hypothesis` (property-based testing)  
**Storage**: Aurora RDS PostgreSQL (Shared table with santiago_munoz_ prefix)  
**Testing**: `pytest`, `hypothesis`, local PostgreSQL containers for integration tests  
**Target Platform**: AWS Lambda (serverless)  
**Project Type**: Bounded Context (Shared Database)  
**Performance Goals**: 
- List operations: <200ms (per SC-002 in PRD)
- Handle 100 concurrent read requests
**Constraints**: 
- Explicit SQL (No ORMs)
- Read-only database access for the query API
- Shared table usage (`santiago_munoz_todos`)
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
| **C-004** | **Persistence**: Read-only repo for Query API using shared table. | ✅ Pass |

## Project Structure

### Documentation (this feature)

```text
specs/002-list-todos/
├── plan.md              # This file
├── research.md          # Query optimization using indexes on write table
├── data-model.md        # Shared schema with prefix
├── quickstart.md        # Setup for Read Side testing
├── contracts/           # OpenAPI definitions (GET /todos)
└── tasks.md             # Implementation tasks
```

### Source Code (repository root)

```text
todo/
  read/                   # todo-read deployment unit
    src/
      entrypoints/        
        api.py           # Lambda handler for GET /todos
      app/               
        queries.py       # Query logic: sort, filter, paginate
      infra/
        db.py            # psycopg connection helpers
        repo.py          # SQL Read repositories
    tests/
      unit/
        test_query_logic.py
      integration/
        test_read_db_e2e.py
```

**Structure Decision**: Using the same tables for read and write reduces infra complexity while maintaining performance through proper indexing.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Shared Table | Reduced architectural overhead for MVP | Denormalized projections were deemed overkill for the current scale. |
