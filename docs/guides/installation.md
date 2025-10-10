# Installation Guide

Detailed installation instructions for knodel.

## System Requirements

- **Python**: 3.13 or higher
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Operating System**: Linux, macOS, or Windows

## Installing uv

knodel uses `uv` for dependency management. The project intentionally has no runtime dependencies beyond the Python standard library. Development tooling (formatting, linting, and testing) is handled by `ruff` and `pytest` through `uv` dependency groups.

### Option 1: Install Script (Linux/macOS - Recommended)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
```

### Option 2: Using pip

```bash
pip install uv
```

### Option 3: Using Homebrew (macOS)

```bash
brew install uv
```

### Verifying Installation

```bash
uv --version
```

## Setting Up knodel

### Clone the Repository

```bash
git clone https://github.com/masriamir/knodel.git
cd knodel
```

### Install Dependencies

#### Using Makefile (Recommended)

```bash
make install
```

This will:
- Sync all dependencies including development and test tools
- Set up the virtual environment
- Prepare the project for development

#### Manual Installation

```bash
uv sync --all-groups
```

**Note**: The first sync may take 3-4 minutes to complete. Don't cancel it!

### Verify Installation

```bash
uv run python -c "import knodel; print('✅ Setup complete')"
```

Or check the version:

```bash
make info
```

## Troubleshooting

### Issue: `uv: command not found`

**Solution**: Ensure `uv` is in your PATH:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Add this to your shell's RC file (`.bashrc`, `.zshrc`, etc.) to make it permanent.

### Issue: Python version mismatch

**Solution**: knodel requires Python 3.13. Check your Python version:

```bash
python --version
```

If you need to install Python 3.13, `uv` can manage Python versions for you:

```bash
uv python install 3.13
```

### Issue: Long installation time

**Explanation**: The first `uv sync --all-groups` can take 3-4 minutes as it downloads and installs all dependencies. This is normal.

### Issue: Cache-related problems

**Solution**: Clean the uv cache:

```bash
make clean
uv cache clean
```

Then try installation again:

```bash
make install
```

## Next Steps

- Follow the [Quick Start Guide](quickstart.md) to run your first session
- Review the [Contributing Guidelines](../contributing/CONTRIBUTING.md) if you want to contribute
- Check out the [Testing Guide](../development/testing.md) to learn about running tests
