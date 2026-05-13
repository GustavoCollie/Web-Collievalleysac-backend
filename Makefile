.PHONY: dev test lint format migrate

dev:
	cd src && uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

test:
	python -m pytest tests/ -v --cov=src --cov-report=term-missing

lint:
	ruff check src/ tests/
	mypy src/

format:
	black src/ tests/
	ruff check src/ tests/ --fix

migrate:
	cd src && alembic upgrade head

migrate-create:
	cd src && alembic revision --autogenerate -m "$(msg)"

seed:
	cd src && python -m infrastructure.persistence.seed
