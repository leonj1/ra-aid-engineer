# Makefile for webhook application

# Variables
TEST_IMAGE_NAME = webhook-tests
DOCKERFILE_TEST = Dockerfile.test

# Colors for pretty output
CYAN = \033[0;36m
GREEN = \033[0;32m
RED = \033[0;31m
NC = \033[0m # No Color

.PHONY: help test clean setup

help: ## Display this help message
	@echo "$(CYAN)Available targets:$(NC)"
	@echo "$(GREEN)test$(NC)   - Run unit tests in Docker container"
	@echo "$(GREEN)setup$(NC)  - Set up git hooks"
	@echo "$(GREEN)clean$(NC)  - Remove Docker test image"
	@echo "$(GREEN)help$(NC)   - Display this help message"

test: ## Run unit tests in Docker container
	@echo "$(CYAN)Building test image...$(NC)"
	docker build -f $(DOCKERFILE_TEST) -t $(TEST_IMAGE_NAME) .
	@echo "$(CYAN)Running tests...$(NC)"
	docker run --rm $(TEST_IMAGE_NAME)

setup: ## Set up git hooks
	@echo "$(CYAN)Setting up git hooks...$(NC)"
	@chmod +x scripts/setup-hooks.sh
	@./scripts/setup-hooks.sh

clean: ## Remove Docker test image
	@echo "$(CYAN)Removing test image...$(NC)"
	docker rmi $(TEST_IMAGE_NAME) || true