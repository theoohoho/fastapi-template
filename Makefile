SHELL := /bin/bash
PYTHON_VERSION ?= "3.9.6"
.DEFAULT_GOAL := help

##@ Dev

api: ## Run api server
	poetry run uvicorn fastapi_template.main:app

api-dev: ## Run api server for dev mode
	poetry run uvicorn fastapi_template.main:app --reload

install: ## Run install
	poetry install

test: ## Run pytest
	poetry run pytest ./fastapi_template/tests/ -vv

mypy: ## Run mypy
	poetry mypy fastapi_template

.PHONY: install run run-dev mypy

##@ Migration

alembic-revision: ## Create a revision
	poetry run alembic revision --autogenerate -m $(msg)


alembic-upgrade: ## Upgrade to head
	poetry run alembic upgrade head

.PHONY: alembic-revision alembic-upgrade

##@ Help

.PHONY: help

help:  ## Display this help	
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<command>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
