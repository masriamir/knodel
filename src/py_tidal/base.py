"""Core abstractions for generating Tidal Cycles code."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable, List, Sequence, Union

TidalPrimitive = Union[str, float, int, bool]


def _format_primitive(value: TidalPrimitive) -> str:
    """Format a primitive Python value as a Tidal friendly string.

    Args:
        value: The raw Python value to convert.

    Returns:
        A string representation that Tidal can parse.
    """

    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


class TidalRenderable(ABC):
    """Protocol for objects that can render themselves as Tidal expressions."""

    @abstractmethod
    def to_tidal(self) -> str:
        """Render the object into a Tidal expression."""

    def __str__(self) -> str:  # pragma: no cover - small proxy
        return self.to_tidal()


@dataclass(frozen=True)
class ControlAssignment(TidalRenderable):
    """Represents the application of a named control to a pattern.

    Attributes:
        name: The control identifier used by Tidal, for example ``cutoff``.
        value: The literal value that should be assigned to ``name``.
    """

    name: str
    value: TidalPrimitive

    def to_tidal(self) -> str:
        """Render the control assignment in Tidal syntax.

        Returns:
            A Tidal ``name value`` expression.
        """

        return f"{self.name} {_format_primitive(self.value)}"


class ControlCollection(TidalRenderable):
    """Groups multiple control assignments into a single renderable block."""

    def __init__(self, assignments: Sequence[ControlAssignment] | None = None):
        self._assignments: List[ControlAssignment] = list(assignments or [])

    def add(self, assignment: ControlAssignment) -> None:
        """Add a new assignment to the collection.

        Args:
            assignment: The assignment to append.
        """

        self._assignments.append(assignment)

    def extend(self, assignments: Iterable[ControlAssignment]) -> None:
        """Add multiple assignments to the collection.

        Args:
            assignments: The assignments to append.
        """

        self._assignments.extend(assignments)

    def to_tidal(self) -> str:
        """Render the entire control collection using the ``#`` operator.

        Returns:
            A formatted string compatible with Tidal ``#`` syntax.
        """

        if not self._assignments:
            return ""
        joined = " # ".join(assignment.to_tidal() for assignment in self._assignments)
        return f"# {joined}"

    def __bool__(self) -> bool:  # pragma: no cover - trivial
        return bool(self._assignments)
