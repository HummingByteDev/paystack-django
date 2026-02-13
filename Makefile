# Makefile for paystack-django development

.PHONY: help install dev-install test lint format type-check clean build publish

help:
	@echo "paystack-django Development Commands"
	@echo "================================="
	@echo ""
	@echo "Setup:"
	@echo "  make install          Install package"
	@echo "  make dev-install      Install with dev dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test             Run tests"
	@echo "  make test-cov         Run tests with coverage"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint             Run linting checks"
	@echo "  make format           Format code with black and isort"
	@echo "  make type-check       Run mypy type checking"
	@echo "  make check-all        Run all checks"
	@echo ""
	@echo "Build & Publish:"
	@echo "  make build            Build distribution"
	@echo "  make publish-test     Publish to TestPyPI"
	@echo "  make publish          Publish to PyPI"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            Remove build artifacts"
	@echo "  make clean-pyc        Remove Python cache files"

install:
	pip install -e .

dev-install:
	pip install -e ".[dev]"

test:
	pytest

test-cov:
	pytest --cov=djpaystack --cov-report=html --cov-report=term-missing

lint:
	flake8 djpaystack --max-line-length=100 --ignore=E203,W503
	black --check djpaystack
	isort --check-only djpaystack

format:
	black djpaystack
	isort djpaystack

type-check:
	mypy djpaystack --ignore-missing-imports

check-all:
	@bash check-all.sh

build: clean
	python -m build
	twine check dist/*

publish-test: build
	twine upload --repository testpypi dist/*

publish: build
	@echo "Publishing to PyPI..."
	@read -p "Are you sure? (yes/no) " confirm && \
	[ "$$confirm" = "yes" ] && \
	twine upload dist/* || echo "Cancelled"

clean: clean-build clean-pyc

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -delete

clean-pyc:
	find . -type f -name '*.py[cod]' -delete
	find . -type f -name '__pycache__' -delete
	find . -name '*~' -delete
	find . -name '.pytest_cache' -delete
	find . -name '.mypy_cache' -delete
	find . -name '.coverage' -delete
	rm -rf htmlcov/

tox:
	tox

docs:
	cd docs && make html
	@echo "Documentation built in docs/_build/html/index.html"

.DEFAULT_GOAL := help
