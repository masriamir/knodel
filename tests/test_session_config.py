"""Unit tests for TidalSession configuration and BPM support."""

from __future__ import annotations

import pytest

from knodel.session import TidalConfig, TidalSession
from knodel.synths import SuperSaw

# Expected CPS for 120 BPM (120 / 60 / 4 = 0.5)
EXPECTED_CPS_120 = 0.5


@pytest.mark.unit
def test_tidal_config_default() -> None:
    """Test TidalConfig with default values."""
    config = TidalConfig()
    assert config.cps is None
    assert config.to_tidal() == ""


@pytest.mark.unit
def test_tidal_config_with_cps() -> None:
    """Test TidalConfig with explicit cps value."""
    config = TidalConfig(cps=EXPECTED_CPS_120)
    assert config.cps == EXPECTED_CPS_120
    assert config.to_tidal() == "setcps 0.5"


@pytest.mark.unit
def test_tidal_config_from_bpm_120() -> None:
    """Test BPM to CPS conversion for 120 BPM."""
    config = TidalConfig.from_bpm(120)
    assert config.cps == EXPECTED_CPS_120  # 120 / 60 / 4 = 0.5
    assert config.to_tidal() == "setcps 0.5"


@pytest.mark.unit
def test_tidal_config_from_bpm_140() -> None:
    """Test BPM to CPS conversion for 140 BPM."""
    config = TidalConfig.from_bpm(140)
    expected_cps = 140 / 60 / 4
    assert config.cps == pytest.approx(expected_cps)
    assert f"setcps {expected_cps}" in config.to_tidal()


@pytest.mark.unit
def test_tidal_config_from_bpm_float() -> None:
    """Test BPM to CPS conversion with float BPM."""
    config = TidalConfig.from_bpm(128.5)
    expected_cps = 128.5 / 60 / 4
    assert config.cps == pytest.approx(expected_cps)


@pytest.mark.unit
def test_session_default_config() -> None:
    """Test TidalSession with default configuration."""
    session = TidalSession()
    assert session.config.cps is None
    # No config should be in output
    output = session.to_tidal()
    assert "setcps" not in output


@pytest.mark.unit
def test_session_with_config() -> None:
    """Test TidalSession with explicit TidalConfig."""
    config = TidalConfig.from_bpm(120)
    session = TidalSession(config=config)
    assert session.config.cps == EXPECTED_CPS_120
    output = session.to_tidal()
    assert "setcps 0.5" in output


@pytest.mark.unit
def test_session_set_bpm() -> None:
    """Test TidalSession.set_bpm() convenience method."""
    session = TidalSession()
    session.set_bpm(120)
    assert session.config.cps == EXPECTED_CPS_120
    output = session.to_tidal()
    assert "setcps 0.5" in output


@pytest.mark.unit
def test_session_set_bpm_float() -> None:
    """Test TidalSession.set_bpm() with float value."""
    session = TidalSession()
    session.set_bpm(135.5)
    expected_cps = 135.5 / 60 / 4
    assert session.config.cps == pytest.approx(expected_cps)


@pytest.mark.unit
def test_session_config_with_patterns() -> None:
    """Test TidalSession output includes config before patterns with blank line."""
    session = TidalSession()
    session.set_bpm(120)
    session.set_stream("d1", SuperSaw().to_pattern())
    session.set_stream("d2", SuperSaw().to_pattern())
    output = session.to_tidal()

    lines = output.split("\n")
    # First line should be setcps
    assert lines[0] == "setcps 0.5"
    # Second line should be blank
    assert lines[1] == ""
    # Remaining lines should be stream assignments
    assert "d1 $" in output
    assert "d2 $" in output


@pytest.mark.unit
def test_session_config_ordering() -> None:
    """Test that config appears before patterns in output."""
    session = TidalSession()
    session.set_bpm(140)
    session.set_stream("d1", SuperSaw().to_pattern())
    output = session.to_tidal()

    # Config should appear before stream assignment
    config_pos = output.find("setcps")
    pattern_pos = output.find("d1 $")
    assert config_pos < pattern_pos


@pytest.mark.unit
def test_session_legacy_configure_still_works() -> None:
    """Test that legacy configure() method still works."""
    session = TidalSession()
    session.configure(setcps="0.7")
    session.set_stream("d1", SuperSaw().to_pattern())
    output = session.to_tidal()
    assert "setcps 0.7" in output
    assert "d1 $" in output


@pytest.mark.unit
def test_session_config_and_legacy_configure() -> None:
    """Test that both TidalConfig and legacy configure work together."""
    session = TidalSession()
    session.set_bpm(120)
    session.configure(other="value")
    output = session.to_tidal()

    # Both should be present
    assert "setcps 0.5" in output
    assert "other value" in output


@pytest.mark.unit
def test_session_no_config_no_blank_line() -> None:
    """Test that no blank line is added when there's no configuration."""
    session = TidalSession()
    session.set_stream("d1", SuperSaw().to_pattern())
    output = session.to_tidal()

    # Should not start with blank line
    assert not output.startswith("\n")
    assert "d1 $" in output


@pytest.mark.unit
def test_session_multiple_bpm_changes() -> None:
    """Test that set_bpm() replaces previous BPM setting."""
    session = TidalSession()
    session.set_bpm(120)
    assert session.config.cps == EXPECTED_CPS_120

    session.set_bpm(140)
    expected_cps = 140 / 60 / 4
    assert session.config.cps == pytest.approx(expected_cps)

    output = session.to_tidal()
    # Should only have the latest BPM
    assert f"setcps {expected_cps}" in output
    # Should not have exactly "setcps 0.5\n" pattern
    assert output.count("setcps") == 1
