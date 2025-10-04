"""Object oriented wrappers around common Tidal synthesizers."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar

from .base import ControlAssignment, ControlCollection, TidalPrimitive
from .patterns import Pattern, SoundPattern


@dataclass(frozen=True)
class SynthParameter:
    """Metadata describing a supported synthesizer control."""

    name: str
    description: str
    default: TidalPrimitive | None = None


class Synth:
    """Base class for defining reusable synthesizer wrappers."""

    sound_name: ClassVar[str]
    parameters: ClassVar[Mapping[str, SynthParameter]] = {}

    def __init__(self, **controls: TidalPrimitive) -> None:
        """Create a new synthesizer instance.

        Args:
            **controls: Control name/value pairs supported by the synth.
        """

        self._validated_controls = self._validate_controls(controls)

    @classmethod
    def _validate_controls(
        cls,
        controls: Mapping[str, TidalPrimitive],
    ) -> dict[str, TidalPrimitive]:
        """Ensure that the provided control names are supported.

        Args:
            controls: Control name/value pairs passed to the constructor.

        Returns:
            A copy of ``controls`` if the names are valid.

        Raises:
            ValueError: If an unknown control name is provided.
        """

        unknown = sorted(set(controls) - set(cls.parameters))
        if unknown:
            raise ValueError(
                f"Unknown control(s) for {cls.__name__}: {', '.join(unknown)}",
            )
        return dict(controls)

    @classmethod
    def describe(cls) -> Mapping[str, SynthParameter]:
        """Return metadata about the synthesizer's controls.

        Returns:
            A mapping of control names to their metadata.
        """

        return dict(cls.parameters)

    def to_pattern(self) -> Pattern:
        """Convert the synthesizer invocation into a :class:`Pattern`.

        Returns:
            A :class:`Pattern` ready for further composition.
        """

        assignments = [
            ControlAssignment(key, value)
            for key, value in self._validated_controls.items()
        ]
        control_collection = ControlCollection(assignments)
        return SoundPattern(self.sound_name, control_collection)

    def to_tidal(self) -> str:
        """Render the synthesizer invocation as a Tidal expression.

        Returns:
            A string representing the synthesizer trigger.
        """

        return self.to_pattern().to_tidal()

    def with_controls(self, **controls: TidalPrimitive) -> Pattern:
        """Produce a new pattern with additional controls applied.

        Args:
            **controls: Extra control assignments to merge.

        Returns:
            A new :class:`Pattern` representing the updated controls.
        """

        merged = {**self._validated_controls, **self._validate_controls(controls)}
        assignments = [ControlAssignment(key, value) for key, value in merged.items()]
        control_collection = ControlCollection(assignments)
        return SoundPattern(self.sound_name, control_collection)


class SuperSaw(Synth):
    """Convenience wrapper for Tidal's ``supersaw`` synthesizer."""

    sound_name = "supersaw"
    parameters: ClassVar[Mapping[str, SynthParameter]] = {
        "cutoff": SynthParameter(
            name="cutoff",
            description="Low pass filter cutoff frequency.",
            default=1000,
        ),
        "resonance": SynthParameter(
            name="resonance",
            description="Resonance amount of the low pass filter.",
            default=0.1,
        ),
        "detune": SynthParameter(
            name="detune",
            description="Detuning factor applied to the saw oscillators.",
            default=0.2,
        ),
    }


class SuperPWM(Synth):
    """Wrapper for the ``superpwm`` synthesizer."""

    sound_name = "superpwm"
    parameters: ClassVar[Mapping[str, SynthParameter]] = {
        "pwidth": SynthParameter(
            name="pwidth",
            description="Pulse width modulation amount.",
            default=0.5,
        ),
        "cutoff": SynthParameter(
            name="cutoff",
            description="Filter cutoff frequency.",
            default=800,
        ),
    }


AVAILABLE_SYNTHS: Mapping[str, type[Synth]] = {
    "supersaw": SuperSaw,
    "superpwm": SuperPWM,
}


__all__ = [
    "AVAILABLE_SYNTHS",
    "SuperPWM",
    "SuperSaw",
    "Synth",
    "SynthParameter",
]
