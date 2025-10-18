# knodel

`knodel` is an experimental toolkit that helps author [Tidal Cycles](https://tidalcycles.org/) patterns using modern Python.
The package offers a set of Pythonic abstractions that mirror the constructs described in the official [Tidal documentation](https://tidalcycles.org/docs/).
This allows the description of musical ideas with familiar object-oriented techniques,
as well as transpiling them into Haskell code that runs inside a live Tidal environment.

## Project goals

* Provide a strongly typed Python façade for common Tidal concepts (patterns, controls, and synthesizers).
* Support ergonomic composition helpers such as stacking and concatenating patterns.
* Offer an extensible transpilation pipeline that can export ready-to-run `.tidal` source files.
* Remain faithful to idiomatic Tidal syntax, so the generated code is immediately recognizable to live-coders.

This repository contains the initial groundwork for these goals. Future iterations can continue to enrich the set of supported synths, controls, and higher-level musical structures.

## Requirements

* Python 3.13
* [uv](https://github.com/astral-sh/uv) for dependency management

The project intentionally has no runtime dependencies beyond the Python standard library. Development tooling (formatting, linting, and testing) is handled by `ruff` and `pytest` through `uv` dependency groups.

## Getting started

```bash
# Install uv if not already available
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# Set up the development environment
make install

# Run the example session
make run

# View the generated Tidal code
cat demo.tidal
```

For detailed setup instructions, see the **[Installation Guide](docs/guides/installation.md)**.

### Running the example session

The `examples` directory contains a minimal session that layers a supersaw,
and a super pulse-width modulation synthesizer pattern.
The Makefile allows transpiling the pattern into Tidal code:

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

For a comprehensive guide on writing sessions, see the **[Quick Start Guide](docs/guides/quickstart.md)**.

## Documentation

For more comprehensive documentation, see:

- 📚 **[Documentation Home](docs/index.md)** - Complete documentation index
- 🚀 **[Quick Start Guide](docs/guides/quickstart.md)** - Get up and running in 5 minutes
- 📦 **[Installation Guide](docs/guides/installation.md)** - Detailed setup instructions
- 👥 **[Contributing Guidelines](docs/contributing/CONTRIBUTING.md)** - How to contribute
- 🔒 **[Security Policy](docs/security/SECURITY.md)** - Reporting vulnerabilities
- 🧪 **[Testing Guide](docs/development/testing.md)** - Writing and running tests
- 📋 **[Release Process](docs/development/releasing.md)** - Version management

## Running tests and linters

```bash
# Run all tests
make test

# Run all quality checks (lint, format-check, type-check, test)
make check

# Auto-fix linting and formatting issues
make fix
```

For detailed testing instructions, see the **[Testing Guide](docs/development/testing.md)**.

## Development

Key development commands:

```bash
make install     # Set up development environment
make check       # Run all quality checks before committing
make fix         # Auto-fix linting and formatting issues
make test        # Run all tests
make build       # Build distribution packages
```

For comprehensive development guidelines, see **[Contributing Guidelines](docs/contributing/CONTRIBUTING.md)**.

## Contributing

Contributions that expand the set of synthesizers, add more pattern combinators, or improve the transpiler are welcome.

**Quick contribution workflow:**

```bash
make install     # Set up environment
# Make any changes
make check       # Verify all checks pass
# Commit and create PR
```

See **[Contributing Guidelines](docs/contributing/CONTRIBUTING.md)** for detailed information on:

- Setting up your development environment
- Development workflow using the Makefile
- Code style guidelines
- Testing requirements
- Pull request process

## Dependency Management

This project uses Dependabot to automatically keep dependencies up to date.
Dependabot will open pull requests weekly with any available updates for the Python dependencies.

All Dependabot PRs must:
- Pass all automated tests (`make test`)
- Pass linting and formatting checks (`make lint` and `make format-check`)
- Be reviewed before merging

To manually update dependencies:
```bash
make install
```

## Release Management

`knodel` uses `hatch-vcs` for automated version management based on **git tags**.

**Creating a release:**

```bash
make release VERSION=0.2.0
```

**Checking the current version:**

```bash
make info    # Shows version and other project information
```

For detailed release instructions and semantic versioning guidelines, see **[Release Process](docs/development/releasing.md)**.

## License

This project uses the [MIT License](LICENSE).
