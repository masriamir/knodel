"""High level session management utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .patterns import Pattern


@dataclass
class StreamAssignment:
    """Represents a mapping between a stream identifier and a pattern."""

    stream: str
    pattern: Pattern

    def to_tidal(self) -> str:
        """Render the assignment in ``d1 $ pattern`` form."""

        return f"{self.stream} $ {self.pattern.to_tidal()}"


class TidalSession:
    """Container that holds multiple stream assignments."""

    def __init__(self) -> None:
        self._assignments: Dict[str, StreamAssignment] = {}
        self._config: Dict[str, str] = {}

    def set_stream(self, stream: str, pattern: Pattern) -> None:
        """Assign a pattern to a stream such as ``d1`` or ``d2``.

        Args:
            stream: The stream identifier recognised by Tidal.
            pattern: The pattern to evaluate on the stream.
        """

        self._assignments[stream] = StreamAssignment(stream=stream, pattern=pattern)

    def configure(self, **options: str | float | int) -> None:
        """Attach raw configuration directives such as ``setcps``.

        Args:
            **options: Key/value pairs that are rendered verbatim.
        """

        for key, value in options.items():
            self._config[key] = str(value)

    def to_tidal(self) -> str:
        """Render the entire session as multiline Tidal source.

        Returns:
            A newline-delimited string of configuration and stream bindings.
        """

        lines = []
        for key, value in self._config.items():
            lines.append(f"{key} {value}")
        for stream in sorted(self._assignments):
            lines.append(self._assignments[stream].to_tidal())
        return "\n".join(lines)


__all__ = ["StreamAssignment", "TidalSession"]
