"""Unit tests for the transpiler pipeline."""

from __future__ import annotations

import pytest

from py_tidal.patterns import Pattern
from py_tidal.session import TidalSession
from py_tidal.synths import SuperPWM, SuperSaw
from py_tidal.transpiler import TidalTranspiler, TranspilerConfig


def test_supersaw_renders_controls() -> None:
    pattern = SuperSaw(cutoff=1000, detune=0.5).to_pattern()
    assert 's "supersaw"' in pattern.to_tidal()
    assert "cutoff 1000" in pattern.to_tidal()
    assert "detune 0.5" in pattern.to_tidal()


def test_stack_combines_patterns() -> None:
    saw = SuperSaw().with_controls(cutoff=1500)
    pwm = SuperPWM().to_pattern()
    stacked = Pattern.stack([saw, pwm])
    assert stacked.to_tidal().startswith("stack [")
    assert "supersaw" in stacked.to_tidal()
    assert "superpwm" in stacked.to_tidal()


def test_session_renders_streams() -> None:
    session = TidalSession()
    session.configure(setcps="0.7")
    session.set_stream("d1", SuperSaw().to_pattern())
    session.set_stream("d2", SuperPWM().to_pattern())
    transpiler = TidalTranspiler(TranspilerConfig(header="-- header"))
    output = transpiler.transpile(session)
    assert output.startswith("-- header")
    assert "d1 $" in output
    assert "d2 $" in output


def test_unknown_control_raises() -> None:
    with pytest.raises(ValueError):
        SuperSaw(foo=1)
