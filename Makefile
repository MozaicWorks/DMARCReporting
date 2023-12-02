.DEFAULT_GOAL := help
.PHONY: help clean install install-dev install-build reformat lint test dist

help: ## Print the help documentation
	@grep -h -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean:
	rm -rf ./dist ./build ./DMARCReporting.egg-info

install: ## Install runtime dependencies
	pipenv install --deploy

install-dev: install ## Install development dependencies
	pipenv install --deploy --dev

install-build: ## Install build dependencies
	pipenv install --deploy --categories="build"

uninstall: ## Uninstall runtime dependencies
	pipenv uninstall --all

uninstall-dev: ## Uninstall development dependencies
	pipenv uninstall --all-dev

lint: ## Check compliance with the style guide
	pipenv run flake8

format: ## Format source and test code using black
	pipenv run black --skip-string-normalization DMARCReporting
	pipenv run black --skip-string-normalization tests

test: lint ## Run unit tests
	pipenv run pytest -vv

dist: clean ## Creates a source distribution and wheel distribution
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine check ./dist/*
	pipenv run check-wheel-contents dist/*.whl

tag: ## Tag version
	$(eval version := $(shell head -n 1 DMARCReporting/__init__.py | sed -e "s/__version__ = //" | sed -e "s/\"//g"))
	git tag -a $(version) -m "Bump version $(version)"
	git push origin master --follow-tags
