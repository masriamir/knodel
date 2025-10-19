"""High level session management utilities."""

from __future__ import annotations

from dataclasses import dataclass

from .patterns import Pattern


@dataclass
class TidalConfig:
    """Configuration parameters for a Tidal Cycles session."""

    cps: float | None = None

    @classmethod
    def from_bpm(cls, bpm: int | float) -> TidalConfig:
        """Create configuration from BPM.

        Formula: cps = bpm / 60 / 4
        Reference: https://tidalcycles.org/docs/reference/cycles/#convert-between-bpm-and-cps

        Args:
            bpm: Beats per minute to convert to cycles per second.

        Returns:
            A TidalConfig instance with the calculated cps value.
        """
        return cls(cps=bpm / 60 / 4)

    def to_tidal(self) -> str:
        """Generate Tidal configuration commands.

        Returns:
            A newline-delimited string of configuration commands.
        """
        commands = []
        if self.cps is not None:
            commands.append(f"setcps {self.cps}")
        return "\n".join(commands)


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

    def __init__(self, config: TidalConfig | None = None) -> None:
        self._assignments: dict[str, StreamAssignment] = {}
        self._config: dict[str, str] = {}
        self.config = config or TidalConfig()

    def set_stream(self, stream: str, pattern: Pattern) -> None:
        """Assign a pattern to a stream such as ``d1`` or ``d2``.

        Args:
            stream: The stream identifier recognized by Tidal.
            pattern: The pattern to evaluate on the stream.
        """

        self._assignments[stream] = StreamAssignment(stream=stream, pattern=pattern)

    def set_bpm(self, bpm: int | float) -> None:
        """Convenience method to set BPM.

        Args:
            bpm: Beats per minute to set for the session.
        """
        self.config = TidalConfig.from_bpm(bpm)

    def configure(self, **options: str | float | int) -> None:
        """Attach raw configuration directives such as ``setcps``.

        Args:
            **options: Key/value pairs stored verbatim.
        """

        for key, value in options.items():
            self._config[key] = str(value)

    def to_tidal(self) -> str:
        """Render the entire session as a multiline Tidal source.

        Returns:
            A newline-delimited string of configuration and stream bindings.
        """

        lines = []

        # Add TidalConfig configuration
        config_code = self.config.to_tidal()
        if config_code:
            lines.append(config_code)

        # Add legacy configuration
        for key, value in self._config.items():
            lines.append(f"{key} {value}")

        # Add blank line if there are any configuration lines
        if lines:
            lines.append("")

        # Add stream assignments
        for stream in sorted(self._assignments):
            lines.append(self._assignments[stream].to_tidal())

        return "\n".join(lines)


__all__ = ["StreamAssignment", "TidalConfig", "TidalSession"]
