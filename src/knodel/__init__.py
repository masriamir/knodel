"""Public package exports for ``knodel``."""

from .patterns import Pattern, SoundPattern
from .session import TidalConfig, TidalSession
from .synths import AVAILABLE_SYNTHS, SuperPWM, SuperSaw, Synth, SynthParameter
from .transpiler import TidalTranspiler, TranspilerConfig

__all__ = [
    "AVAILABLE_SYNTHS",
    "Pattern",
    "SoundPattern",
    "SuperPWM",
    "SuperSaw",
    "Synth",
    "SynthParameter",
    "TidalConfig",
    "TidalSession",
    "TidalTranspiler",
    "TranspilerConfig",
]

try:
    from knodel._version import __version__
except ImportError:
    __version__ = "0.0.0+unknown"
