# Contributing to Chai Sutta

Thank you for your interest in contributing! This guide will help you get set up and understand our workflow.

---

## Table of Contents

- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Commit Convention](#commit-convention)
- [Database Migrations](#database-migrations)
- [Writing Tests](#writing-tests)
- [Pull Request Process](#pull-request-process)

---

## Development Setup

### 1. Fork and clone

```bash
git clone https://github.com/<your-username>/Chai-Sutta.git
cd Chai-Sutta
```

### 2. Install dependencies

We use [`uv`](https://github.com/astral-sh/uv) for fast package management.

```bash
pip install uv
uv venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate          # Windows
uv pip install -e ".[dev]"
```

### 3. Start infrastructure services

```bash
docker compose up postgres redis qdrant -d
```

### 4. Configure environment

```bash
cp .env.example .env
# Edit .env with your values
```

### 5. Run migrations and seed

```bash
make migrate
make seed
```

### 6. Start the dev server

```bash
make dev
```

Visit `http://localhost:8000/docs` to confirm the API is running.

---

## Project Structure

```
app/
├── api/v1/          # REST endpoints — one file per domain
├── core/            # Infrastructure: DB, Redis, Qdrant, security, geo
├── models/          # SQLAlchemy ORM models (one per entity)
├── schemas/         # Pydantic request/response schemas
├── workers/         # ARQ background tasks
│   └── tasks/       # Individual task modules
└── scripts/         # One-off scripts (seeding, etc.)
```

Each domain (news, weather, traffic, etc.) follows this pattern:
- `models/<domain>.py` — DB model
- `schemas/<domain>.py` — Pydantic schemas
- `api/v1/<domain>.py` — FastAPI router

---

## Coding Standards

We use **Ruff** for both linting and formatting. All code must pass before a PR can be merged.

```bash
make format   # Format + auto-fix
make lint     # Check for lint errors
```

### Rules enforced

- `E`, `F`, `W` — pycodestyle/pyflakes errors and warnings
- `I` — isort import ordering
- `N` — PEP8 naming
- `UP` — pyupgrade (modern Python syntax)
- `ANN` — type annotations (ANN101/102/401 excluded)
- `B` — flake8-bugbear
- `A` — flake8-builtins
- `SIM` — flake8-simplify

### Type annotations

All functions and methods must have type annotations on parameters and return types. Use `from __future__ import annotations` at the top of each file.

### Docstrings

- Module-level docstrings are required.
- All public functions and classes need docstrings (Google style preferred).
- Private helpers (`_method`) may have brief one-liners.

### Async

All I/O-bound code must be `async`. Do not use blocking calls in endpoint handlers or worker tasks.

---

## Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short summary>

[optional body]

[optional footer]
```

### Types

| Type | When to use |
|---|---|
| `feat` | New feature or endpoint |
| `fix` | Bug fix |
| `chore` | Tooling, config, deps, scripts |
| `docs` | Documentation only |
| `refactor` | Code change with no feature/fix |
| `test` | Adding or fixing tests |
| `migration` | New Alembic migration |
| `perf` | Performance improvement |

### Examples

```
feat(reports): add nearby reports endpoint with PostGIS spatial query
fix(auth): prevent login with deactivated accounts
chore(deps): bump fastapi to 0.115.5
docs(readme): update quickstart guide
migration: add event location column
```

---

## Database Migrations

We use Alembic for schema migrations. **Never edit existing migrations** — always create a new one.

### Create a migration

```bash
make migrate-create
# Enter a descriptive message when prompted
# e.g.: "add user preferences column"
```

This runs `alembic revision --autogenerate` using your model changes.

### Apply migrations

```bash
make migrate
# or
alembic upgrade head
```

### Rules

- One migration per PR (unless unavoidable)
- Never drop columns without a deprecation period
- Spatial columns must use GeoAlchemy2 types

---

## Writing Tests

Tests live in `app/tests/` and use:
- `pytest` + `pytest-asyncio` for async tests
- `pytest-cov` for coverage reporting

```bash
make test
# or
pytest -v --cov=app --cov-report=term-missing
```

### Test naming conventions

```
app/tests/
├── test_auth.py
├── test_reports.py
├── test_news.py
└── ...
```

### Example test

```python
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

### Coverage target

Aim for **≥ 80%** coverage on new modules. Critical paths (auth, reports CRUD) should be near **100%**.

---

## Pull Request Process

1. **Branch off `main`**:
   ```bash
   git checkout -b feat/your-feature-name
   ```

2. **Write code** following the standards above.

3. **Run checks locally**:
   ```bash
   make format
   make lint
   make test
   ```

4. **Commit** with conventional commit messages.

5. **Push** and open a PR against `main`.

6. **PR description** should include:
   - What changed and why
   - Any breaking changes
   - How to test it
   - Screenshots (for UI-adjacent changes)

7. **Checklist** before requesting review:
   - [ ] `make lint` passes
   - [ ] `make test` passes
   - [ ] New migrations are included (if schema changed)
   - [ ] Docs updated (if API surface changed)
   - [ ] `.env.example` updated (if new env vars added)

---

## Questions?

Open a [GitHub Discussion](https://github.com/ayyushutup/Chai-Sutta/discussions) or file an [Issue](https://github.com/ayyushutup/Chai-Sutta/issues).
