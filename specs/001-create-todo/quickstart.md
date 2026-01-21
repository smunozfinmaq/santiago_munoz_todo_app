# Quickstart: US-001: Create Todo

## Local Development Setup

### Prerequisites
- Python 3.11+
- Docker (for PostgreSQL integration tests)

### 1. Install Dependencies
```bash
# From repository root
pip install -r todo/write/requirements.txt
pip install -r todo/write/requirements-dev.txt
```

### 2. Run Unit Tests (TDD/Property-Based)
```bash
# Run domain logic tests
pytest todo/write/tests/unit
```

### 3. Run Integration Tests
```bash
# Start a local postgres container
docker run --name todo-db -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15

# Run integration tests
export DATABASE_URL="postgresql://postgres:password@localhost:5432/postgres"
pytest todo/write/tests/integration
```

## Implementation Workflow
1. Define the domain model in `todo/write/src/domain/model.py`.
2. Write unit tests for creation invariance in `todo/write/tests/unit/test_domain_properties.py`.
3. Implement the Command Handler in `todo/write/src/app/create_todo_command.py`.
4. Implement the SQL repository in `todo/write/src/infra/repo.py`.
5. Connect everything in the Lambda handler `todo/write/src/entrypoints/api.py`.
