# Implementation Plan: US-001: Create Todo

**Branch**: `001-create-todo` | **Date**: 2026-01-20 | **Spec**: [specs/001-create-todo/spec.md](spec.md)
**Input**: Feature specification from `/specs/001-create-todo/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement the "Create Todo" functionality using a CQRS-based serverless architecture. The system will handle command-side writes (creating todos) with transactional integrity in Aurora PostgreSQL and emit events for read-side projection updates. The implementation focuses on serverless testability, idempotency, and explicit SQL over ORMs.

## Technical Context

**Language/Version**: Python 3.11+ (AWS Lambda runtime)  
**Primary Dependencies**: `psycopg` (PostgreSQL driver), `aws-lambda-powertools` (Python), `pytest` (testing), `hypothesis` (property-based testing)  
**Storage**: Aurora RDS PostgreSQL (authoritative datastore in `santiago_munoz_write` schema)  
**Testing**: `pytest`, `hypothesis` (property-based testing), local PostgreSQL containers for integration tests  
**Target Platform**: AWS Lambda (serverless), Aurora PostgreSQL  
**Project Type**: Bounded Context (CQRS pattern with write/read separation)  
**Performance Goals**: 
- Create/retrieve operations: <2 seconds (per SC-001)
- State change log retrieval: <1 second (per SC-005)
- Handle 10 concurrent operations without data loss (per SC-003)
**Constraints**: 
- All writes must be transactional
- Idempotent command handling (mandatory)
- Soft DELETE only
- No ORMs (explicit SQL only)
- Lambda handlers must be thin adapters
- Business logic must be testable without AWS dependencies
**Scale/Scope**: 
- Single-user or user-agnostic service (no multi-tenancy)
- No authentication/authorization required
- Reasonable data volumes (standard web service assumptions)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Requirement | Status |
|------|-------------|--------|
| **C-001** | **Simplicity**: No speculative abstractions or ORM usage. | ✅ Pass |
| **C-002** | **Serverless Testability**: Business logic isolated from Lambda runtime. | ✅ Pass |
| **C-003** | **Testing Strategy**: Property-based testing via `hypothesis` mandated. | ✅ Pass |
| **C-004** | **Persistence**: Side effects (SQL) isolated in infra layer; No ORMs. | ✅ Pass |
| **C-005** | **Idempotency**: Mandatory handling of command duplicates. | ✅ Pass |

## Project Structure

### Documentation (this feature)

```text
specs/001-create-todo/
├── plan.md              # This file
├── research.md          # Implementation details for idempotency and PostgreSQL patterns
├── data-model.md        # Entity definitions and SQL schema
├── quickstart.md        # Local setup with PostgreSQL containers
├── contracts/           # API Gateway / OpenAPI definitions
└── tasks.md             # Implementation tasks
```

### Source Code (repository root)

```text
todo/                     # Bounded Context name
  db/                     # Sqitch project for schema migrations
    deploy/
    revert/
    verify/
  write/                  # todo-write deployment unit (Command Side)
    src/
      entrypoints/        # AWS glue: api.py (Lambda handler)
      app/                # Use-cases: commands.py, create_todo_command.py, command_handler.py
      domain/             # Pure logic: model.py (Aggregate), events.py
      infra/              # Side effects: db.py (psycopg), repo.py (SQL), outbox.py
    tests/                # Unit (Hypothesis) and Integration (Postgres container) tests
  read/                   # todo-read deployment unit (Query Side)
    src/
      entrypoints/        # api.py (Queries), consume_events.py (Projection updater)
      app/                # queries.py, projections.py
      infra/              # db.py, repo.py
    tests/                # Unit and Integration tests
```

**Structure Decision**: The CQRS bounded context structure separates write-side command handling (domain logic + events) from read-side query serving. This ensures high throughput on reads, deterministic logic on writes, and full testability of the domain without cloud infrastructure.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| CQRS Pattern | High scalability and auditability requirements | Simple CRUD lacks easy event sourcing/outbox support for future growth. |
| No ORM | Performance and explicit control over SQL/Transactions | ORMs introduce magic and make optimization harder in serverless environments. |
