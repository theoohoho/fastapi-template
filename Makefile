SHELL := /bin/bash
PYTHON_VERSION ?= "3.9.6"
.DEFAULT_GOAL := help

##@ Dev

run: ## Run api server
	poetry run uvicorn main:app

run-dev: ## Run api server for dev mode
	poetry run uvicorn main:app --reload

install:
	poetry install

.PHONY: install run run-dev

##@ Help

.PHONY: help

help:  ## Display this help	
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<command>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
