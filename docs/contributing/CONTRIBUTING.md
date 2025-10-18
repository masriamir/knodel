# Contributing to `knodel`

This document outlines guidelines and instructions for contributing to this project.

## Getting Started

### Prerequisites

- Python 3.13
- [uv](https://github.com/astral-sh/uv) package manager

### Setting Up Your Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/masriamir/knodel.git
   cd knodel
   ```

2. Install uv (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   export PATH="$HOME/.local/bin:$PATH"
   ```

3. Set up the development environment:
   ```bash
   make install
   ```
   
   This will sync all dependencies, including development and test tools.

## Development Workflow

A Makefile will standardize common development tasks. Here are the most important commands:

### Quick Reference

```bash
make help          # Display all available commands
make install       # Set up the development environment
make test          # Run all tests
make check         # Run all quality checks (lint, format-check, type-check, test)
make fix           # Auto-fix linting and formatting issues
```

### Running Tests

```bash
# Run all tests
make test

# Run tests verbosely
make test ARGS="-v"

# Run specific test file
make test ARGS="tests/test_synths.py"

# Run tests marked with a specific marker
make test ARGS="-m unit"

# Run specific test
make test ARGS="tests/test_synths.py::TestSuperSaw"
```

### Code Quality

Before committing code, ensure it passes all quality checks:

```bash
# Run all checks (recommended before committing)
make check
```

This runs:
- Linting with ruff
- Format checking with ruff
- Type checking with mypy
- All tests

Run individual quality checks as needed:

```bash
make lint           # Check code for issues
make format-check   # Check code formatting
make type-check     # Run static type checking
```

### Formatting and Linting

```bash
# Auto-fix all fixable issues (linting + formatting)
make fix

# Or run them separately:
make lint-fix       # Fix linting issues
make format         # Format code
```

### Building and Running

```bash
# Build distribution packages
make build

# Run the example session
make run

# Run with custom output file
make run OUTPUT=my_session.tidal
```

### Project Information

```bash
# Display project information (version, git commit, Python version, etc.)
make info
```

### Cleaning Up

```bash
# Remove build artifacts, caches, and generated files
make clean
```

## Pre-Commit Checklist

Before committing any changes, please ensure:

- [ ] All tests pass: `make test`
- [ ] Code formatted properly: `make format-check` (or run `make fix`)
- [ ] No linting errors: `make lint` (or run `make fix`)
- [ ] Type checking passes: `make type-check`
- [ ] Alternatively, run: `make check` to verify all of the above

## Code Style Guidelines

### Python Style

- Follow PEP 8, and the project's ruff configuration
- Use double quotes for strings
- Maximum line length: 88 characters
- Use Google-style docstrings for functions and classes

### Type Hints

- All public functions should have type hints
- Use modern Python type hint syntax (Python 3.13+)

### Testing

- Write tests for all new functionality
- Use descriptive test names: `test_<function>_<scenario>_<expected>`
- Mark tests appropriately with `@pytest.mark.unit` or other markers
- Test both success and failure cases

## Pull Request Process

1. Fork the repository and create a new branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make any changes and ensure all checks pass:
   ```bash
   make check
   ```

3. Commit the changes with a descriptive commit message:
   ```bash
   git commit -m "#99 Add feature: brief description"
   ```

4. Push the fork and submit a pull request

5. Ensure your PR description clearly describes:
   - What were the changes?
   - What was the rationale for the changes?
   - How to test them?
   - Any breaking changes

6. Link relevant issues using keywords: `Closes #123`, `Fixes #456`, or `Resolves #789`

## Adding New Features

### Adding a New Synthesizer

1. Create a class in `src/knodel/synths.py` inheriting from `BaseSynth`
2. Define controls as dataclass fields
3. Implement the `to_tidal()` method
4. Add unit tests in `tests/test_synths.py`
5. Update documentation if needed

### Adding a New Pattern Transformation

1. Add a method to the `Pattern` class in `src/knodel/patterns.py`
2. Return a new `Pattern` instance with the transformed expression
3. Add tests demonstrating the Tidal output

## Release Process

The `hatch-vcs` plugin will _automatically_ manage new releases using **git tags**.

For maintainers creating a release:

```bash
# Ensure all changes are committed
git status

# Run all checks
make check

# Create and push a release tag
make release VERSION=0.2.0
```

This will:
1. Run all quality checks
2. Create an annotated git tag
3. Push the tag to origin
4. Build distribution packages

## Getting Help

- Open an issue for bugs or feature requests
- Check existing issues before creating a new one
- Be respectful and constructive in all interactions

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions

## License

By agreeing to contribute to `knodel`, _any_ contributions will be licensed under the **MIT License**.
