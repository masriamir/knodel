"""Example session demonstrating the high level API."""

from __future__ import annotations

from knodel.patterns import Pattern
from knodel.session import TidalSession
from knodel.synths import SuperPWM, SuperSaw


def create_session() -> TidalSession:
    """Create a simple session layering two synthesizer patterns."""

    session = TidalSession()
    supersaw = SuperSaw(cutoff=1200, detune=0.4).to_pattern()
    pwm = SuperPWM(pwidth=0.7).to_pattern().fast(2)
    session.configure(setcps="0.6")
    session.set_stream("d1", Pattern.stack([supersaw, pwm]))
    return session
