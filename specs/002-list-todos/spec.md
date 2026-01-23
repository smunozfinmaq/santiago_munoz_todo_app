# Feature Specification: US-002: List Todos (pagination, filtering, sorting)

**Feature Branch**: `002-list-todos`  
**Created**: 2026-01-22  
**Status**: Draft  
**Jira Issue**: [TB-3](https://squad-core-mark.atlassian.net/browse/TB-3)
**PRD Reference**: [PRD-000: Todo Management System PRD](https://squad-core-mark.atlassian.net/spaces/IDP/pages/270761985)

## Context (PRD traceability)

- **PRD §2 User Scenarios & Testing**: P1 List Todos
- **PRD §3 Functional Requirements**: (11) pagination, (12) filter by status, (18) sort by `created_at` or `due_date`
- **PRD §5 API Specification**: `GET /todos`

## User Story

As a user, I want to list my todos with pagination and basic query options, so that I can browse tasks efficiently.

**Priority**: P1

## Clarifying Questions & Answers

- **What are the default and max values for page and limit?**  
  Answer: Default `page=1`, `limit=10`. Max `limit=100`.
- **What is the response shape for pagination?**  
  Answer:
  ```json
  {
    "items": [...],
    "metadata": {
      "total_count": 25,
      "page": 2,
      "limit": 10,
      "total_pages": 3
    }
  }
  ```
- **What is the exact filter parameter for status?**  
  Answer: `?status=completed` (maps to `is_completed=true`) and `?status=pending` (maps to `is_completed=false`).
- **What is the sort parameter format?**  
  Answer: `?sort=created_at|due_date` and `?order=asc|desc`. Default is `sort=created_at&order=desc`.
- **Should soft-deleted todos be excluded?**  
  Answer: Yes, by default.

## User Scenarios & Testing

### Scenario: List first page with defaults
**Given** an identified user context exists  
**And** the user has multiple todos  
**When** the client sends `GET /todos`  
**Then** the response status is 200  
**And** the response items are ordered by `created_at` descending  
**And** pagination metadata shows `page: 1` and `limit: 10`.

### Scenario: List with explicit pagination
**Given** an identified user context exists  
**And** the user has 25 todos  
**When** the client sends `GET /todos?page=2&limit=10`  
**Then** the response status is 200  
**And** the response returns 10 items  
**And** metadata shows `total_count: 25`, `page: 2`, `total_pages: 3`.

### Scenario: Filter by Completed
**Given** an identified user context exists  
**And** the user has both completed and pending todos  
**When** the client sends `GET /todos?status=completed`  
**Then** the response status is 200  
**And** every returned todo has `is_completed: true`.

### Scenario: Sort by due date ascending
**Given** an identified user context exists  
**And** the user has todos with different due dates  
**When** the client sends `GET /todos?sort=due_date&order=asc`  
**Then** the response status is 200  
**And** todos are ordered by increasing `due_date` (tasks without `due_date` appear last).

### Scenario: Reject invalid pagination parameters
**Given** an identified user context exists  
**When** the client sends `GET /todos?page=0&limit=-1`  
**Then** the response status is 400  
**And** the error indicates invalid pagination values.

## Requirements

### Functional Requirements

- **FR-001**: System MUST support `page` and `limit` query parameters for pagination.
- **FR-002**: System MUST default pagination to `page=1` and `limit=10` if not provided.
- **FR-003**: System MUST support filtering by status: `completed` or `pending`.
- **FR-004**: System MUST support sorting by `created_at` (default) or `due_date`.
- **FR-005**: System MUST support sort order `asc` or `desc` (default).
- **FR-006**: System MUST return pagination metadata including `total_count` and `total_pages`.
- **FR-007**: System MUST validate query parameters and return 400 for invalid inputs.

## Success Criteria

- **SC-001**: API returns correctly paginated results for 100% of valid requests.
- **SC-002**: Filtering by status correctly restricts the results.
- **SC-003**: Sorting follows the requested field and order correctly.
- **SC-004**: Metadata accurately reflects the total dataset size and current position.
