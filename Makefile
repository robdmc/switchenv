#! /usr/bin/env make 

SHELL := /usr/bin/env bash


.PHONY: help 
help:  ## Print the help documentation
	@grep -E '^[a-zA-Z_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.PHONY: uv_env
uv_env: ## Create an env for this project
	rm -rf .venv || true
	uv venv

.PHONY: uv_lock
uv_lock:  ## Create lock file
	uv lock

.PHONY: uv_sync
uv_sync: ## Installs lock file into env (creating lockfile if needed)
	uv sync --extra dev

.PHONY: uv_activate
uv_activate: ## Activate the virtual environment
	@exec bash --rcfile <(echo '. ~/.bashrc; source .venv/bin/activate; echo "Virtual environment activated"')

.PHONY: uv_nuke
uv_nuke: ## Delete the virtual environment
	rm -rf .venv || true


.PHONY: clean
clean:  ## Remove build artifacts, caches, and coverage results
	rm -rf dist/ build/ *.egg-info
	rm -rf htmlcov/ .coverage
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type d -name '.pytest_cache' -exec rm -rf {} +

.PHONY: uv_build
uv_build: ## Build the package using UV
	uv build

.PHONY: uv_publish
uv_publish: uv_build ## Publish the package to PyPI using twine
	uv run twine upload dist/*

.PHONY: uv_publish_test
uv_publish_test: uv_build ## Publish the package to TestPyPI using twine
	uv run twine upload --repository testpypi dist/*

.PHONY: tag_show
tag_show:  ## Show all git tags
	git tag | cat -
