### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-xeu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

IMAGE_NAME=ghcr.io/kitconcept/cluster-purger
IMAGE_TAG=latest

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build: ## Build codebase
	@echo -en "$(GREEN)==> Build Codebase$(RESET)"
	@echo ""
	@poetry install

# Dev Tools
.PHONY: format
format: ## Format codebase
	@echo -en "$(GREEN)==> Format codebase$(RESET)"
	@echo ""
	@poetry run black cluster_purger/
	@poetry run isort cluster_purger/

.PHONY: lint
lint: ## Lint codebase
	@echo -en "$(GREEN)==> Lint codebase$(RESET)"
	@echo ""
	@poetry run black --check --diff cluster_purger/
	@poetry run isort --check-only cluster_purger/
	@poetry run flakeheaven lint cluster_purger/

.PHONY: test
test: ## Test codebase
	@echo -en "$(GREEN)==> Test codebase$(RESET)"
	@echo ""
	@poetry run pytest

# Docker Support
.PHONY: build-image
build-image: ## Creates a new Docker image
	@echo -en "$(GREEN)==> Creating Application Image!$(RESET)"
	@echo ""
	@docker buildx build -t $(IMAGE_NAME):$(IMAGE_TAG) -f Dockerfile .


.PHONY: start-image
start-image: build-image ## Start Docker Image
	@echo -en "$(GREEN)==> Starting Application Image!$(RESET)"
	@echo ""
	@docker run -it -p 8000:8000 $(IMAGE_NAME):$(IMAGE_TAG)
