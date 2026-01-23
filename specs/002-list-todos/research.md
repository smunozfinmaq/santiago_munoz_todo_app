# Research: US-002: List Todos

## Domain Analysis: Query Side (Read Models)

### Decision: Direct Reading from Write Table
- **Problem**: Deciding between a denormalized read model and direct reading from the write table.
- **Solution**: To simplify the architecture for the current scope, the List Todos Lambda will read directly from the `santiago_munoz_todos` table.
- **Rationale**: Minimal latency for current requirements and reduced architectural complexity by removing event-driven projections.

## Technology Best Practices

### PostgreSQL Dynamic SQL
- **Decision**: Use `psycopg`'s `sql` module for safe dynamic query building (for filters and sorting).
- **Rationale**: Avoids SQL injection while allowing flexible `WHERE` and `ORDER BY` clauses.

### Property-Based Testing for Pagination
- **Decision**: Use `hypothesis` to test that `page_1_items + page_2_items == all_items` for various offsets/limits.
- **Rationale**: High confidence in pagination logic correctness.

## Integration Research

### PowerTools for API Response
- **Decision**: Use `aws-lambda-powertools` for structured logging and potentially for response formatting.
- **Rationale**: Consistency across the codebase.
