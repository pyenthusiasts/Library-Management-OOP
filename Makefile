.PHONY: help install install-dev test test-cov lint format clean run docker-build docker-up docker-down backup restore

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install:  ## Install the package
	pip install -e .

install-dev:  ## Install package with development dependencies
	pip install -e ".[dev]"
	pre-commit install

test:  ## Run tests
	pytest -v

test-cov:  ## Run tests with coverage
	pytest --cov=library_system --cov-report=html --cov-report=term

test-watch:  ## Run tests in watch mode
	pytest-watch

lint:  ## Run all linting tools
	flake8 library_system tests --max-line-length=100 --extend-ignore=E203,W503
	mypy library_system --ignore-missing-imports
	pylint library_system

format:  ## Format code with black and isort
	black library_system tests examples
	isort library_system tests examples

format-check:  ## Check code formatting without making changes
	black --check library_system tests examples
	isort --check-only library_system tests examples

clean:  ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	rm -rf build dist

run:  ## Run the CLI application
	library-cli

run-demo:  ## Run the CLI with demo data
	library-cli --demo

run-example-basic:  ## Run basic usage example
	python examples/basic_usage.py

run-example-advanced:  ## Run advanced usage example
	python examples/advanced_usage.py

docker-build:  ## Build Docker image
	docker build -t library-management-system:latest .

docker-up:  ## Start Docker containers
	docker-compose up -d

docker-down:  ## Stop Docker containers
	docker-compose down

docker-logs:  ## View Docker logs
	docker-compose logs -f

backup:  ## Backup library data
	@echo "Creating backup..."
	@mkdir -p backups
	@cp data/library_data.json backups/library_data_$$(date +%Y%m%d_%H%M%S).json 2>/dev/null || echo "No data file to backup"
	@cp logs/*.log backups/ 2>/dev/null || echo "No log files to backup"
	@echo "Backup complete!"

restore:  ## Restore library data from latest backup
	@echo "Available backups:"
	@ls -1 backups/library_data_*.json 2>/dev/null || echo "No backups found"
	@echo "To restore, copy the desired backup to data/library_data.json"

check-deps:  ## Check for outdated dependencies
	pip list --outdated

update-deps:  ## Update dependencies
	pip install --upgrade pip
	pip install --upgrade -e ".[dev]"

pre-commit:  ## Run pre-commit hooks on all files
	pre-commit run --all-files

docs:  ## Generate documentation
	@echo "API documentation available in docs/API.md"
	@echo "README available in README.md"

init-db:  ## Initialize database (if using SQLite)
	@echo "Initializing database..."
	python -c "from library_system.services.database_service import init_db; init_db()"

migrate:  ## Run database migrations
	@echo "Running migrations..."
	python scripts/migrate_data.py

ci:  ## Run CI checks (lint, format-check, test)
	@echo "Running CI checks..."
	$(MAKE) format-check
	$(MAKE) lint
	$(MAKE) test-cov
	@echo "All checks passed!"

setup:  ## Complete project setup
	@echo "Setting up Library Management System..."
	$(MAKE) install-dev
	@cp .env.example .env 2>/dev/null || echo ".env already exists"
	@mkdir -p logs data backups config
	@echo "Setup complete! Edit .env file with your configuration."
	@echo "Run 'make run-demo' to try the application."

all:  ## Run format, lint, and test
	$(MAKE) format
	$(MAKE) lint
	$(MAKE) test-cov
