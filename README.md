# knodel

`knodel` is an experimental toolkit that helps you author [Tidal Cycles](https://tidalcycles.org/) patterns using modern Python. The package offers a set of Pythonic abstractions that mirror the constructs described in the official [Tidal documentation](https://tidalcycles.org/docs/) so that you can describe musical ideas with familiar object-oriented techniques and transpile them into Haskell code that runs inside a live Tidal environment.

## Project goals

* Provide a strongly-typed Python façade for common Tidal concepts (patterns, controls, and synthesizers).
* Support ergonomic composition helpers such as stacking and concatenating patterns.
* Offer an extensible transpilation pipeline that can export ready-to-run `.tidal` source files.
* Remain faithful to idiomatic Tidal syntax so the generated code is immediately recognisable to live-coders.

This repository contains the initial groundwork for these goals. Future iterations can continue to enrich the set of supported synths, controls, and higher-level musical structures.

## Requirements

* Python 3.13
* [uv](https://github.com/astral-sh/uv) for dependency management

The project intentionally has no runtime dependencies beyond the Python standard library. Development tooling (formatting, linting, and testing) is handled by `ruff` and `pytest` through `uv` dependency groups.

## Getting started

### Quick Start

The project uses a Makefile for streamlined development workflow:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# Set up development environment
make install

# Run the example session
make run

# View the generated Tidal code
cat demo.tidal
```

### Manual Setup (Alternative)

If you prefer not to use the Makefile, you can set up manually:

```bash
uv sync --all-groups
```

### Running the example session

The `examples` directory contains a minimal session that layers a supersaw and a super pulse-width modulation synthesizer pattern. You can transpile it into Tidal code using the Makefile:

```bash
make run                    # Creates demo.tidal
make run OUTPUT=my.tidal    # Creates my.tidal
```

Or directly with the CLI:

```bash
uv run python -m knodel examples.basic_session:create_session --output demo.tidal
cat demo.tidal
```

The generated file is ready to be loaded into a running Tidal Cycles interpreter.

### Writing your own sessions

1. Import the provided primitives:
   ```python
   from knodel.patterns import Pattern
   from knodel.session import TidalSession
   from knodel.synths import SuperSaw
   ```
2. Instantiate synthesizer wrappers, optionally configuring their controls.
3. Use the pattern helpers (e.g., `stack`, `fast`, `slow`) to build complex layers.
4. Add the resulting patterns to a `TidalSession` and transpile using `TidalTranspiler`.

For example:

```python
from knodel.patterns import Pattern
from knodel.session import TidalSession
from knodel.synths import SuperPWM, SuperSaw

session = TidalSession()
supersaw = SuperSaw(cutoff=1200, detune=0.4).to_pattern()
pwm = SuperPWM(pwidth=0.7).to_pattern().fast(2)
session.configure(setcps="0.6")
session.set_stream("d1", Pattern.stack([supersaw, pwm]))
```

Finally, call `TidalTranspiler` to generate the Haskell snippet:

```python
from pathlib import Path
from knodel.transpiler import TidalTranspiler

transpiler = TidalTranspiler()
output = transpiler.transpile(session)
Path("session.tidal").write_text(output, encoding="utf-8")
```

## Running tests and linters

### Using the Makefile (Recommended)

The Makefile provides convenient commands for all development tasks:

```bash
# Run all tests
make test

# Run tests with custom arguments
make test ARGS="-v"                           # Verbose output
make test ARGS="-m unit"                      # Run only unit tests
make test ARGS="tests/test_synths.py"         # Run specific test file

# Run all quality checks (lint, format-check, type-check, test)
make check

# Auto-fix linting and formatting issues
make fix

# Individual checks
make lint           # Run linting checks
make format-check   # Check code formatting
make type-check     # Run type checking

# Other useful commands
make help           # Display all available commands
make info           # Show project information
make clean          # Clean build artifacts and caches
```

### Manual Commands (Alternative)

If you prefer not to use the Makefile, you can run commands manually:

```bash
# Tests
uv run pytest

# Linting and formatting
uv run ruff check .
uv run ruff format .

# Type checking
uv run mypy .
```

## Development

For detailed development guidelines, workflow, and contribution instructions, please see [CONTRIBUTING.md](CONTRIBUTING.md).

Key development commands:

```bash
make install     # Set up development environment
make check       # Run all quality checks before committing
make fix         # Auto-fix linting and formatting issues
make test        # Run all tests
make build       # Build distribution packages
```

## Contributing

Contributions that expand the set of synthesizers, add more pattern combinators, or improve the transpiler are welcome. Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:

- Setting up your development environment
- Development workflow using the Makefile
- Code style guidelines
- Testing requirements
- Pull request process

**Quick contribution workflow:**

```bash
make install     # Set up environment
# Make your changes
make check       # Verify all checks pass
# Commit and create PR
```

## Dependency Management

This project uses Dependabot to automatically keep dependencies up-to-date. Dependabot will open pull requests weekly with any available updates for our Python dependencies.

All Dependabot PRs must:
- Pass all automated tests (`uv run pytest`)
- Pass linting and formatting checks (`uv run ruff check .` and `uv run ruff format --check .`)
- Be reviewed before merging

To manually update dependencies:
```bash
uv sync --all-groups
```

## Release Management

`knodel` uses `hatch-vcs` for automated version management based on git tags. Version numbers are derived from git tags following semantic versioning (semver) principles.

**Version Numbering:**
- Tagged releases: Version matches the git tag (e.g., tag v0.2.0 becomes version 0.2.0)
- Development builds: Commits after a tag receive a .devN suffix with the commit hash (e.g., 0.2.0.dev3+gabcd123)
- Version format: Follows PEP 440 and semantic versioning (MAJOR.MINOR.PATCH)

**Creating a New Release:**

Using the Makefile (recommended):

```bash
# Ensure all changes are committed
git status

# Create and push a release
make release VERSION=0.2.0
```

This will automatically:
1. Run all quality checks
2. Create an annotated git tag
3. Push the tag to origin
4. Build distribution packages

Manual release process:

1. Ensure all changes are committed and pushed (git status should show clean working tree)
2. Run pre-release checks: `make check`
3. Create an annotated tag following semantic versioning:
   - For new features (minor version bump): `git tag -a v0.2.0 -m "Release 0.2.0: Add pattern sequencing support"`
   - For bug fixes (patch version bump): `git tag -a v0.1.1 -m "Release 0.1.1: Fix transpiler edge cases"`
   - For breaking changes (major version bump): `git tag -a v1.0.0 -m "Release 1.0.0: Stable API with breaking changes"`
4. Push the tag to trigger release: `git push origin v0.2.0`
5. Build distribution packages: `make build`

**Checking Current Version:**

To check the current version of knodel:

```bash
make info    # Shows version and other project info
```

Or manually:
- In Python: `import knodel; print(knodel.__version__)`
- From command line: `uv run python -c "import knodel; print(knodel.__version__)"`

Note: The version is automatically imported from the auto-generated `src/knodel/_version.py` file. You should always import the `knodel` package (not `_version.py` directly) to access the version.

**Semantic Versioning Guidelines:**
- MAJOR (1.0.0): Incompatible API changes or breaking changes
- MINOR (0.2.0): New functionality in a backwards-compatible manner
- PATCH (0.1.1): Backwards-compatible bug fixes

For more information, see Semantic Versioning 2.0.0 at semver.org.

## License

This project is licensed under the terms of the [MIT License](LICENSE).
