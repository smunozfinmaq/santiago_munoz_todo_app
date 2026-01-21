# Feature Specification: US-001: Create Todo

**Feature Branch**: `001-create-todo`  
**Created**: 2026-01-20  
**Status**: Draft  
**Jira Issue**: [TB-2](https://squad-core-mark.atlassian.net/browse/TB-2)
**PRD Reference**: [PRD-000: Todo Management System PRD](https://squad-core-mark.atlassian.net/spaces/IDP/pages/270761985)

## Context (PRD traceability)

- **PRD §2 User Scenarios & Testing**: P1 Create Todo
- **PRD §3 Functional Requirements**: (6) create todo with title (required) + description (optional), (10) priority, (19) timestamps
- **PRD §4 Key Entities**: `Todo` attributes include `title`, `description`, `priority`, `due_date`, `created_at`
- **PRD §5 API Specification**: `POST /todos`

## User Story

As a user, I want to create a todo with a required title and optional details, so that I can capture tasks I need to do.

**Priority**: P1

## Clarifying Questions & Answers

- **What are the title validation rules?**  
  Answer: Max 500 characters.
- **Is description plain text only, and is there a max length?**  
  Answer: Plain text, max 500 characters.
- **Are priority and due_date optional, and what are their defaults?**  
  Answer: Both optional, default to empty values (treat as null unless specified).
- **What is the allowed due_date format?**  
  Answer: ISO-8601 required (e.g., 2026-01-20T12:00:00Z).
- **Should the create response include updated_at?**  
  Answer: Yes, the entity table should include it.
- **Should clients be allowed to set is_completed at creation?**  
  Answer: Defaults to false.

## User Scenarios & Testing

### Scenario: Create todo with title only (default values)
**Given** an identified user context exists  
**When** the client sends `POST /todos` with body `{ "title": "Buy milk" }`  
**Then** the response status is 201  
**And** the response JSON includes:  
- `title: "Buy milk"`  
- `description: null`  
- `priority: null`  
- `due_date: null`  
- `is_completed: false`  
- `created_at` (server-generated timestamp)  
- `updated_at` (server-generated timestamp)

### Scenario: Create todo with all fields
**Given** an identified user context exists  
**When** the client sends `POST /todos` with body:
```json
{
  "title": "Buy milk",
  "description": "2% fat",
  "priority": "High",
  "due_date": "2026-01-20T12:00:00Z"
}
```
**Then** the response status is 201  
**And** the response JSON matches the input values  
**And** `is_completed` is `false`

### Scenario: Reject create when title is empty
**Given** an identified user context exists  
**When** the client sends `POST /todos` with an empty title or missing title field  
**Then** the response status is 400  
**And** the response JSON is a consistent error object  
**And** the error indicates title is required

### Scenario: Reject create when title exceeds 500 characters
**Given** an identified user context exists  
**When** the client sends `POST /todos` with a title length of 501 characters  
**Then** the response status is 400  
**And** the error indicates title exceeds maximum length

### Scenario: Reject create when priority is invalid
**Given** an identified user context exists  
**When** the client sends `POST /todos` with body `{ "title": "Task", "priority": "Urgent" }`  
**Then** the response status is 400  
**And** the error indicates priority must be one of Low, Medium, High

## Requirements

### Functional Requirements

- **FR-001**: System MUST allow users to create a todo with a required title (max 500 characters).
- **FR-002**: System MUST allow optional plain text description (max 500 characters).
- **FR-003**: System MUST allow optional priority (Low, Medium, High).
- **FR-004**: System MUST allow optional due date in ISO-8601 format.
- **FR-005**: System MUST default `is_completed` to `false`.
- **FR-006**: System MUST automatically generate `id` (UUID), `created_at`, and `updated_at`.
- **FR-007**: System MUST return consistent JSON error objects for all 400 responses.

### Key Entities

- **Todo**:
  - `id`: UUID (Required, system-generated).
  - `title`: String, max 500 (Required).
  - `description`: String, max 500 (Optional).
  - `priority`: Enum (Low, Medium, High) (Optional).
  - `due_date`: ISO-8601 String (Optional).
  - `is_completed`: Boolean (Default: false).
  - `created_at`: Timestamp (Required).
  - `updated_at`: Timestamp (Required).

## Success Criteria

- **SC-001**: Users can successfully create a todo with valid input (P1 flow).
- **SC-002**: Validation correctly rejects invalid inputs (empty title, long strings, bad formats) with status 400.
- **SC-003**: System response includes all audit timestamps and system-generated IDs.

