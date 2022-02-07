.DEFAULT_GOAL := help
.PHONY: help install install-dev install-build lint test dist

help: ## Print the help documentation
	@grep -h -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## Install runtime dependencies
	pip install --upgrade pip
	pip install -r requirements.txt

install-dev: install ## Install development dependencies
	pip install -r requirements-dev.txt

install-build: ## Install build dependencies
	pip install -r requirements-build.txt

lint: ## Check compliance with the style guide
	flake8

test: lint ## Run unit tests
	pytest -vv

dist: ## Creates a source distribution and wheel distribution
	python setup.py sdist bdist_wheel
	twine check ./dist/*
	check-wheel-contents dist/*.whl
