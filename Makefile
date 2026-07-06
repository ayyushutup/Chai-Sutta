# ============================================
# Chai Sutta - Makefile
# ============================================

.PHONY: dev up down migrate migrate-create seed test lint format worker clean

# --- Development ---
dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# --- Docker ---
up:
	docker compose up -d --build

down:
	docker compose down -v

# --- Database Migrations ---
migrate:
	alembic upgrade head

migrate-create:
	@read -p "Migration message: " msg; \
	alembic revision --autogenerate -m "$$msg"

# --- Seed Data ---
seed:
	python -m app.scripts.seed

# --- Testing ---
test:
	pytest -v --cov=app --cov-report=term-missing

# --- Linting & Formatting ---
lint:
	ruff check app/

format:
	ruff format app/
	ruff check --fix app/

# --- Background Worker ---
worker:
	arq app.workers.worker.WorkerSettings

# --- Cleanup ---
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf dist/ build/ htmlcov/ .coverage coverage.xml
