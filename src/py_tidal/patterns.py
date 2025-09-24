"""Pattern primitives that closely mirror the Tidal DSL."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from .base import ControlCollection, ControlAssignment, TidalRenderable


@dataclass(frozen=True)
class Pattern(TidalRenderable):
    """Represents a Tidal pattern expression."""

    expression: str

    def to_tidal(self) -> str:
        """Render the underlying expression string."""

        return self.expression

    def with_controls(self, *assignments: ControlAssignment) -> Pattern:
        """Attach control assignments to the pattern using ``#``.

        Args:
            *assignments: Controls to append to the pattern.

        Returns:
            A new :class:`Pattern` with the assignments appended.
        """

        control_collection = ControlCollection(assignments)
        suffix = f" {control_collection.to_tidal()}" if control_collection else ""
        return Pattern(f"{self.expression}{suffix}")

    def slow(self, factor: int | float) -> Pattern:
        """Apply the ``slow`` function to the pattern.

        Args:
            factor: The rate divider to apply.

        Returns:
            A new :class:`Pattern` slowed by ``factor``.
        """

        return Pattern(f"slow {factor} $ {self.expression}")

    def fast(self, factor: int | float) -> Pattern:
        """Apply the ``fast`` function to the pattern.

        Args:
            factor: The rate multiplier to apply.

        Returns:
            A new :class:`Pattern` accelerated by ``factor``.
        """

        return Pattern(f"fast {factor} $ {self.expression}")

    def degrade(self) -> Pattern:
        """Apply ``degrade`` which randomly drops events.

        Returns:
            A new :class:`Pattern` that will stochastically drop events.
        """

        return Pattern(f"degrade $ {self.expression}")

    @staticmethod
    def stack(patterns: Iterable[TidalRenderable]) -> Pattern:
        """Layer multiple patterns using the ``stack`` combinator.

        Args:
            patterns: The patterns to layer on top of each other.

        Returns:
            A :class:`Pattern` representing the stacked layers.
        """

        rendered: List[str] = [pattern.to_tidal() for pattern in patterns]
        joined = ", ".join(rendered)
        return Pattern(f"stack [{joined}]")

    @staticmethod
    def cat(patterns: Iterable[TidalRenderable]) -> Pattern:
        """Concatenate multiple patterns using ``cat``.

        Args:
            patterns: The patterns to concatenate sequentially.

        Returns:
            A :class:`Pattern` that cycles through the concatenated patterns.
        """

        rendered: List[str] = [pattern.to_tidal() for pattern in patterns]
        joined = ", ".join(rendered)
        return Pattern(f"cat [{joined}]")


class SoundPattern(Pattern):
    """Specialised ``Pattern`` that represents a Tidal synthesizer trigger."""

    def __init__(self, sound_name: str, controls: ControlCollection | None = None):
        controls = controls or ControlCollection()
        suffix = f" {controls.to_tidal()}" if controls else ""
        super().__init__(f's "{sound_name}"{suffix}')


__all__ = ["Pattern", "SoundPattern"]
