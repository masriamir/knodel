"""Test build and cache integrity."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.unit
def test_uv_cache_configuration_exists() -> None:
    """Verify uv cache configuration is present in pyproject.toml."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    content = pyproject_path.read_text()

    assert "[tool.uv]" in content, "Missing [tool.uv] section"
    assert "cache-keys" in content, "Missing cache-keys configuration"
    assert "{ git = { commit = true, tags = true } }" in content, (
        "Git-based cache keys not configured"
    )


@pytest.mark.unit
def test_version_accessible_after_install() -> None:
    """Verify version is accessible after fresh install (cache test)."""
    result = subprocess.run(  # noqa: S603
        [sys.executable, "-c", "import knodel; print(knodel.__version__)"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, f"Failed to import version: {result.stderr}"
    assert result.stdout.strip(), "Version string is empty"
    # Version should either be a tag (0.1.0) or dev version (0.1.0.dev1+g...)
    version = result.stdout.strip()
    assert "." in version, f"Invalid version format: {version}"
