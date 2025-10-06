# Makefile for knodel development workflow automation
# This Makefile provides a standardized interface for common development tasks

# Variables
PYTHON := uv run python
PYTEST := uv run pytest
RUFF := uv run ruff
MYPY := uv run mypy
UV := uv

# Color output support
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

# Default values for parameters
OUTPUT ?= demo.tidal
ARGS ?=
VERSION ?=

# Default target
.DEFAULT_GOAL := help

# Phony targets (targets that don't create files)
.PHONY: help install lint lint-fix format format-check type-check test build run info clean check fix coverage watch-test docs release

# Help target - displays all available commands with descriptions
help:
	@echo "$(BLUE)Available make targets:$(NC)"
	@echo ""
	@echo "$(GREEN)Core Commands:$(NC)"
	@echo "  make lint           - Run linting checks with ruff"
	@echo "  make lint-fix       - Run linting checks with auto-fix"
	@echo "  make format         - Format code with ruff"
	@echo "  make format-check   - Check formatting without modifying"
	@echo "  make type-check     - Run type checking with mypy"
	@echo "  make test           - Run tests (use ARGS=\"-v\" for verbose)"
	@echo "  make build          - Build distribution packages"
	@echo "  make run            - Run example session (use OUTPUT=file.tidal)"
	@echo "  make info           - Display project information"
	@echo ""
	@echo "$(GREEN)Additional Commands:$(NC)"
	@echo "  make install        - Set up development environment"
	@echo "  make clean          - Clean build artifacts and caches"
	@echo "  make check          - Run all quality checks (lint, format-check, type-check, test)"
	@echo "  make fix            - Auto-fix all fixable issues"
	@echo "  make coverage       - Run tests with coverage report"
	@echo "  make watch-test     - Run tests in watch mode (requires pytest-watch)"
	@echo "  make docs           - Build documentation (placeholder)"
	@echo "  make release        - Create a release (use VERSION=0.2.0)"
	@echo ""
	@echo "$(YELLOW)Examples:$(NC)"
	@echo "  make test ARGS=\"-v\"                        - Run tests verbosely"
	@echo "  make test ARGS=\"-m unit\"                  - Run unit tests only"
	@echo "  make test ARGS=\"tests/test_synths.py\"     - Run specific test file"
	@echo "  make run OUTPUT=my.tidal                    - Generate my.tidal"
	@echo "  make release VERSION=0.2.0                  - Create v0.2.0 release"

# Install - set up development environment
install:
	@echo "$(BLUE)Setting up development environment...$(NC)"
	@$(UV) sync --all-groups
	@echo "$(GREEN)✓ Development environment ready$(NC)"

# Lint - run linting checks
lint:
	@echo "$(BLUE)Running linting checks...$(NC)"
	@$(RUFF) check .
	@echo "$(GREEN)✓ Linting passed$(NC)"

# Lint-fix - run linting checks with auto-fix
lint-fix:
	@echo "$(BLUE)Running linting checks with auto-fix...$(NC)"
	@$(RUFF) check --fix .
	@echo "$(GREEN)✓ Linting completed with fixes applied$(NC)"

# Format - format code
format:
	@echo "$(BLUE)Formatting code...$(NC)"
	@$(RUFF) format .
	@echo "$(GREEN)✓ Code formatted$(NC)"

# Format-check - check formatting without modifying
format-check:
	@echo "$(BLUE)Checking code formatting...$(NC)"
	@$(RUFF) format --check .
	@echo "$(GREEN)✓ Formatting check passed$(NC)"

# Type-check - run type checking
type-check:
	@echo "$(BLUE)Running type checks...$(NC)"
	@$(MYPY) .
	@echo "$(GREEN)✓ Type checking passed$(NC)"

# Test - run tests with optional arguments
test:
	@echo "$(BLUE)Running tests...$(NC)"
	@$(PYTEST) $(ARGS)
	@echo "$(GREEN)✓ Tests passed$(NC)"

# Build - build distribution packages
build:
	@echo "$(BLUE)Building distribution packages...$(NC)"
	@$(UV) build
	@echo "$(GREEN)✓ Build completed$(NC)"

# Run - run the example session
run:
	@echo "$(BLUE)Running example session...$(NC)"
	@$(PYTHON) -m knodel examples.basic_session:create_session --output $(OUTPUT)
	@echo "$(GREEN)✓ Generated $(OUTPUT)$(NC)"

# Info - display project information
info:
	@echo "$(BLUE)Project Information:$(NC)"
	@echo "  Project:     knodel"
	@echo -n "  Version:     " && $(PYTHON) -c "import knodel; print(knodel.__version__)" 2>/dev/null || echo "unknown"
	@echo -n "  Git Commit:  " && git rev-parse --short HEAD 2>/dev/null || echo "unknown"
	@echo -n "  Branch:      " && git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown"
	@echo -n "  Python:      " && $(PYTHON) --version 2>/dev/null || echo "unknown"
	@echo -n "  uv:          " && $(UV) --version 2>/dev/null || echo "unknown"
	@if git diff --quiet 2>/dev/null; then \
		echo "  Status:      $(GREEN)Clean$(NC)"; \
	else \
		echo "  Status:      $(YELLOW)Uncommitted changes$(NC)"; \
	fi

# Clean - clean build artifacts and caches
clean:
	@echo "$(BLUE)Cleaning build artifacts and caches...$(NC)"
	@rm -rf dist/ build/ *.egg-info
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/
	@rm -f *.tidal
	@echo "$(GREEN)✓ Cleanup completed$(NC)"

# Check - run all quality checks
check: lint format-check type-check test
	@echo "$(GREEN)✓ All checks passed$(NC)"

# Fix - auto-fix all fixable issues
fix:
	@echo "$(BLUE)Auto-fixing issues...$(NC)"
	@$(RUFF) check --fix .
	@$(RUFF) format .
	@echo "$(GREEN)✓ All fixes applied$(NC)"

# Coverage - run tests with coverage report
coverage:
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	@$(PYTEST) --cov=knodel --cov-report=term-missing
	@echo "$(GREEN)✓ Coverage report generated$(NC)"

# Watch-test - run tests in watch mode
watch-test:
	@echo "$(BLUE)Running tests in watch mode...$(NC)"
	@$(UV) run ptw

# Docs - build documentation (placeholder)
docs:
	@echo "$(YELLOW)Documentation building not yet configured.$(NC)"
	@echo "This is a placeholder for future Sphinx/MkDocs integration."

# Release - create a release
release:
	@if [ -z "$(VERSION)" ]; then \
		echo "$(RED)Error: VERSION not specified. Use: make release VERSION=0.2.0$(NC)"; \
		exit 1; \
	fi
	@echo "$(BLUE)Creating release v$(VERSION)...$(NC)"
	@echo "$(BLUE)Validating version...$(NC)"
	@if git tag -l v$(VERSION) | grep -q .; then \
		echo "$(RED)Error: Tag v$(VERSION) already exists$(NC)"; \
		exit 1; \
	fi
	@PACKAGE_VERSION=$$($(PYTHON) -c "import knodel; print(knodel.__version__.split('+')[0].replace('.dev', ''))" 2>/dev/null || echo ""); \
	if [ -n "$$PACKAGE_VERSION" ] && [ "$$PACKAGE_VERSION" != "$(VERSION)" ]; then \
		echo "$(YELLOW)Warning: Package version ($$PACKAGE_VERSION) differs from release version ($(VERSION))$(NC)"; \
		echo "$(YELLOW)This is expected for new releases. Proceeding...$(NC)"; \
	fi
	@echo "$(BLUE)Running pre-release checks...$(NC)"
	@$(MAKE) check
	@if [ -n "$$(git status --porcelain)" ]; then \
		echo "$(RED)Error: Uncommitted changes or untracked files. Commit, stash, or remove them first.$(NC)"; \
		exit 1; \
	fi
	@echo "$(BLUE)Creating git tag v$(VERSION)...$(NC)"
	@git tag -a v$(VERSION) -m "Release $(VERSION)"
	@echo "$(BLUE)Pushing tag to origin...$(NC)"
	@git push origin v$(VERSION)
	@echo "$(BLUE)Building distribution...$(NC)"
	@$(MAKE) build
	@echo "$(GREEN)✓ Release v$(VERSION) created successfully$(NC)"
	@echo "$(YELLOW)Note: Distribution packages are in dist/$(NC)"
