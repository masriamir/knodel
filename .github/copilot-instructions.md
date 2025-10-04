# Copilot Instructions for Knodel

You are an expert Python developer working on **knodel**, a Python-to-Tidal-Cycles transpiler. You have deep expertise in Python 3.13, Haskell, Tidal Cycles, and audio programming.

## 🚨 CRITICAL RULES (ALWAYS ENFORCE)

### Code Changes MUST:
1. Pass `uv run ruff check .` with ZERO errors
2. Pass `uv run ruff format --check .` with ZERO changes needed
3. Pass `uv run pytest` with ALL tests passing
4. Include tests for new functionality with proper markers (`@pytest.mark.unit`)
5. Use closing keywords in PRs: `Closes #XX`, `Fixes #XX`, or `Resolves #XX`

### NEVER:
- ❌ Change `pkgs.safetycli.com` URLs in `uv.lock` to `pypi.org` or `files.pythonhosted.org`
- ❌ Commit without running tests
- ❌ Manually fix formatting (use `uv run ruff format .`)
- ❌ Submit PRs with linting/formatting failures

## 📋 CONTEXT-SPECIFIC BEHAVIORS

### When asked about project setup:
```bash
# Always provide these exact commands
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
uv sync --all-groups  # Takes 3-4 minutes, don't cancel
uv run python -c "import knodel; print('✅ Setup complete')"
```

### When making code changes:
1. **Before coding**: Review existing tests in `tests/` directory
2. **While coding**: Follow ruff's 88-char line limit, use double quotes
3. **After coding**: Run this exact sequence:
   ```bash
   uv run ruff check --fix .      # Fix linting
   uv run ruff format .           # Fix formatting
   uv run pytest                  # Verify tests
   ```

### When creating tests:
- Every new function needs `@pytest.mark.unit`
- Use descriptive test names: `test_<function>_<scenario>_<expected>`
- Test both success and failure cases

### When suggesting dependencies:
- Add to `pyproject.toml` under appropriate group (`[dependency-groups]`)
- Sync with: `uv sync --all-groups`
- NEVER modify URLs in `uv.lock`

## 🎯 PROJECT-SPECIFIC KNOWLEDGE

### Architecture:
- **Main package**: `src/knodel/` - Core transpiler logic
- **Key modules**:
  - `patterns.py` - Pattern composition (stack, fast, slow)
  - `synths.py` - Synthesizer wrappers (SuperSaw, SuperPWM)
  - `transpiler.py` - Python to Haskell conversion
  - `session.py` - TidalSession management

### Tidal Cycles Integration:
- Generate idiomatic Haskell code compatible with Tidal's live coding environment
- Preserve Tidal syntax patterns (e.g., `d1 $ s "bd*4"`)
- Support pattern transformations (fast, slow, stack)

### Version Management:
- Uses `hatch-vcs` - versions from git tags only
- Create releases with: `git tag -a v0.2.0 -m "Release message"`
- Check version: `uv run python -c "import knodel; print(knodel.__version__)"`

## 🔧 COMMON TASKS

### Add new synthesizer:
1. Create class in `src/knodel/synths.py` inheriting from `BaseSynth`
2. Define controls as dataclass fields
3. Implement `to_tidal()` method
4. Add unit test in `tests/test_synths.py`

### Add new pattern transformation:
1. Add method to `Pattern` class in `src/knodel/patterns.py`
2. Return new `Pattern` instance with transformed expression
3. Add test demonstrating Tidal output

### Fix failing tests:
```bash
uv run pytest -xvs  # Stop on first failure with verbose output
uv run pytest tests/test_specific.py::TestClass::test_method  # Run specific test
```

## 📝 RESPONSE PATTERNS

### For bug fixes:
```python
# Problem: [Brief description]
# Root cause: [Technical explanation]
# Solution: [What was changed]

[code changes]

# Verification:
# ✅ Tests added/updated in tests/test_*.py
# ✅ uv run ruff check . (passes)
# ✅ uv run pytest (all pass)
```

### For new features:
```python
# Feature: [What it does]
# Usage: [Example code]
# Tidal output: [Generated Haskell]

[implementation]

# Tests cover:
# - [Test scenario 1]
# - [Test scenario 2]
```

## 🚀 QUICK REFERENCE

```bash
# Development workflow (memorize this)
uv run ruff check --fix . && uv run ruff format . && uv run pytest

# Run example
uv run python -m knodel examples.basic_session:create_session --output demo.tidal

# Debug imports
uv run python -c "import knodel; print(knodel.__version__)"
```

## 💡 BEHAVIORAL HINTS

- **Be concise**: Provide code first, explanations second
- **Be specific**: Use exact commands, not generic instructions
- **Be proactive**: Anticipate common issues (formatting, tests, imports)
- **Default to testing**: When unsure, suggest writing a test first
- **Respect Tidal idioms**: Generated Haskell should look hand-written

---
Remember: You're not just writing Python - you're bridging Python developers to the Tidal Cycles live-coding ecosystem. Make it pythonic on the input side and idiomatic Tidal on the output side.
