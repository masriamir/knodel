"""Example session demonstrating BPM configuration."""

from __future__ import annotations

from knodel.patterns import Pattern
from knodel.session import TidalConfig, TidalSession
from knodel.synths import SuperPWM, SuperSaw


def create_session_with_bpm() -> TidalSession:
    """Create a session with BPM configuration using the new TidalConfig API."""

    # Method 1: Set BPM directly with convenience method
    session = TidalSession()
    session.set_bpm(140)

    supersaw = SuperSaw(cutoff=1200, detune=0.4).to_pattern()
    pwm = SuperPWM(pwidth=0.7).to_pattern().fast(2)
    session.set_stream("d1", Pattern.stack([supersaw, pwm]))
    return session


def create_session_with_config() -> TidalSession:
    """Create a session with TidalConfig passed to constructor."""

    # Method 2: Create session with BPM configuration
    config = TidalConfig.from_bpm(120)
    session = TidalSession(config=config)

    session.set_stream("d1", SuperSaw(cutoff=1500).to_pattern())
    session.set_stream("d2", SuperPWM(pwidth=0.6).to_pattern())
    return session


def create_session_with_cps() -> TidalSession:
    """Create a session with direct CPS setting for advanced users."""

    # Method 3: Set CPS directly for advanced users
    config = TidalConfig(cps=0.5)
    session = TidalSession(config=config)

    session.set_stream("d1", SuperSaw().to_pattern())
    return session
