.PHONY: help install test lint format type-check run run-worker clean

help:
	@echo "Softkillbot - Development Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make install        - Install dependencies"
	@echo "  make test          - Run tests"
	@echo "  make test-coverage - Run tests with coverage"
	@echo "  make lint          - Run linters"
	@echo "  make format        - Format code"
	@echo "  make type-check    - Run type checking"
	@echo "  make run           - Run bot locally"
	@echo "  make run-worker    - Run Celery worker"
	@echo "  make docker-up     - Start Docker services"
	@echo "  make docker-down   - Stop Docker services"
	@echo "  make clean         - Clean up temporary files"

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v

test-coverage:
	pytest tests/ -v --cov=src --cov-report=html

lint:
	flake8 src tests
	pylint src tests

format:
	black src tests
	isort src tests

type-check:
	mypy src

run:
	python -m src.bot.main

run-worker:
	celery -A src.workers.celery_app worker --loglevel=info

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	rm -rf .pytest_cache .coverage htmlcov
