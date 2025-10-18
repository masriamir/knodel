# Release Management

How knodel manages versions and releases.

## Overview

`knodel` uses `hatch-vcs` for automated version management based on **git tags**.
Version numbers derive from **git tags** following semantic versioning (semver) principles.

## Version Numbering

### Tagged Releases

Version matches the git tag (e.g., tag `v0.2.0` becomes version `0.2.0`)

### Development Builds

Commits after a tag receive a `.devN` suffix with the commit hash (e.g., `0.2.0.dev3+gabcd123`)

### Version Format

Follows PEP 440 and semantic versioning (MAJOR.MINOR.PATCH)

## Creating a New Release

### Using the Makefile (Recommended)

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

### Manual Release Process

Without using the Makefile:

1. **Ensure a clean working tree**
   ```bash
   git status  # Should show no uncommitted changes
   ```

2. **Run pre-release checks**
   ```bash
   make check
   ```

3. **Create annotated tag** following semantic versioning:
   
   For new features (minor version bump):
   ```bash
   git tag -a v0.2.0 -m "Release 0.2.0: Add pattern sequencing support"
   ```
   
   For bug fixes (patch version bump):
   ```bash
   git tag -a v0.1.1 -m "Release 0.1.1: Fix transpiler edge cases"
   ```
   
   For breaking changes (major version bump):
   ```bash
   git tag -a v1.0.0 -m "Release 1.0.0: Stable API with breaking changes"
   ```

4. **Push the tag** to trigger release:
   ```bash
   git push origin v0.2.0
   ```

5. **Build distribution packages**
   ```bash
   make build
   ```

## Semantic Versioning Guidelines

knodel follows [Semantic Versioning 2.0.0](https://semver.org/):

### MAJOR version (1.0.0)

Increment when an incompatible API change or breaking change occurs.

**Examples:**
- Removing or renaming public API methods
- Changing function signatures
- Removing support for a Python version

### MINOR version (0.2.0)

Increment when adding any backwards-compatible _functionality_.

**Examples:**
- Adding new synthesizers
- Adding new pattern combinators
- Adding new features
- Enhancing existing features without breaking changes

### PATCH version (0.1.1)

Increment when making any backwards-compatible _bug fixes_.

**Examples:**
- Fixing transpiler edge cases
- Correcting documentation
- Fixing bugs without changing the API

## Checking Current Version

### Using Makefile

```bash
make info
```

This shows the version and other project information.

### Manually

In Python:
```python
import knodel
print(knodel.__version__)
```

From the command line:
```bash
uv run python -c "import knodel; print(knodel.__version__)"
```

**Note**: The auto-generated `src/knodel/_version.py` file controls the library version.
Always import the `knodel` package (not `_version.py` directly) to access the version.

## Release Checklist

For maintainers creating a release:

- [ ] All changes are committed and pushed
- [ ] Working tree is clean (`git status`)
- [ ] All tests pass (`make test`)
- [ ] All quality checks pass (`make check`)
- [ ] CHANGELOG updated (if applicable)
- [ ] Version number follows semantic versioning
- [ ] Tag message is descriptive
- [ ] Tag pushed to origin
- [ ] Distribution packages built
- [ ] GitHub release created (optional)

## Post-Release

After a successful release:

1. Verify the tag appears in GitHub
2. Check that CI/CD passed
3. Announce the release (if significant)
4. Update documentation if needed

## Troubleshooting

### Issue: Version not updating after tag

**Solution**: Ensure the tag is an annotated tag (use `-a` flag) and is pushed to origin:

```bash
git tag -a v0.2.0 -m "Release message"
git push origin v0.2.0
```

### Issue: Release checks fail

**Solution**: Fix the issues before creating the release:

```bash
make check  # See what is failing
make fix    # Auto-fix where possible
```

### Issue: Tag already exists

**Solution**: Delete the tag locally and remotely, then recreate:

```bash
git tag -d v0.2.0                # Delete the tag locally
git push origin :refs/tags/v0.2.0  # Delete the tag remotely
git tag -a v0.2.0 -m "Release message"
git push origin v0.2.0
```

## Related Documentation

- [Contributing Guidelines](../contributing/CONTRIBUTING.md)
- [Testing Guide](testing.md)
- [Semantic Versioning](https://semver.org/)
