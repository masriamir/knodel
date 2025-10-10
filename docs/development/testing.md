# Testing Guide

Comprehensive guide to testing in knodel.

## Overview

knodel uses `pytest` for testing, `ruff` for linting and formatting, and `mypy` for type checking. All tests should pass before committing changes.

## Running Tests

### Using Makefile (Recommended)

```bash
# Run all tests
make test

# Run tests verbosely
make test ARGS="-v"

# Run only unit tests
make test ARGS="-m unit"

# Run specific test file
make test ARGS="tests/test_synths.py"

# Run specific test
make test ARGS="tests/test_synths.py::TestSuperSaw"
```

### Manual Commands

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=knodel --cov-report=term-missing
```

## Code Quality Checks

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

### Individual Checks

```bash
make lint           # Check code for issues
make format-check   # Check code formatting
make type-check     # Run static type checking
```

### Auto-fixing Issues

```bash
# Auto-fix all fixable issues (linting + formatting)
make fix

# Or run them separately:
make lint-fix       # Fix linting issues
make format         # Format code
```

## Writing Tests

### Test Structure

Tests should follow these conventions:

- Place tests in the `tests/` directory
- Use descriptive test names: `test_<function>_<scenario>_<expected>`
- Mark tests appropriately with `@pytest.mark.unit` or other markers
- Test both success and failure cases

### Example Test

```python
import pytest
from knodel.synths import SuperSaw

@pytest.mark.unit
def test_supersaw_creates_valid_pattern():
    """Test that SuperSaw creates a valid pattern."""
    saw = SuperSaw(note="c4", cutoff=1200)
    pattern = saw.to_pattern()
    assert pattern is not None
    assert "supersaw" in pattern.expression

@pytest.mark.unit
def test_supersaw_invalid_control_raises():
    """Test that invalid control raises an error."""
    with pytest.raises(ValueError):
        SuperSaw(invalid_control=123)
```

### Test Markers

Available pytest markers:

- `@pytest.mark.unit` - Unit tests (fast, no I/O)
- Add more markers as needed in `pytest.ini`

## Pre-Commit Checklist

Before committing your changes, please ensure:

- [ ] All tests pass: `make test`
- [ ] Code is properly formatted: `make format-check` (or run `make fix`)
- [ ] No linting errors: `make lint` (or run `make fix`)
- [ ] Type checking passes: `make type-check`
- [ ] Or simply run: `make check` to verify all of the above

## Coverage Reports

Generate a coverage report to see which code is tested:

```bash
make coverage
```

This will run tests and display a coverage report showing:
- Lines covered by tests
- Lines missing coverage
- Overall coverage percentage

## Watch Mode

For continuous testing during development:

```bash
make watch-test
```

This requires `pytest-watch` to be installed (included in dev dependencies).

## Testing Best Practices

1. **Write tests first**: Consider writing tests before implementing features (TDD)
2. **Keep tests simple**: Each test should verify one specific behavior
3. **Use descriptive names**: Test names should clearly describe what they test
4. **Test edge cases**: Include tests for boundary conditions and error cases
5. **Avoid test interdependence**: Tests should be able to run in any order
6. **Mock external dependencies**: Use mocks for I/O, network calls, etc.

## Debugging Failed Tests

### Run specific test with verbose output

```bash
uv run pytest -xvs tests/test_specific.py::test_name
```

Flags:
- `-x`: Stop on first failure
- `-v`: Verbose output
- `-s`: Show print statements

### Use pytest's debugging features

```bash
# Drop into debugger on failure
uv run pytest --pdb

# Drop into debugger on first failure
uv run pytest -x --pdb
```

## CI/CD Testing

All tests automatically run in GitHub Actions on:
- Pull requests
- Pushes to main branch
- Tag creation

Ensure your changes pass locally before pushing to avoid CI failures.

## Related Documentation

- [Contributing Guidelines](../contributing/CONTRIBUTING.md)
- [Release Process](releasing.md)
