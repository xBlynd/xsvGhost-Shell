from typing import Any


class HeartbeatEngine:
    """The Immune System.

    Phoenix base:
    - Tracks simple beat counter
    - Provides a status snapshot of core subsystems
    """

    def __init__(self, kernel: Any) -> None:
        self.kernel = kernel
        self.beats = 0

    def tick(self) -> None:
        self.beats += 1

    def status(self) -> dict:
        """Return a lightweight status snapshot.

        Future: expand with per-engine health, last error, etc.
        """
        return {
            "beats": self.beats,
            "os_type": self.kernel.os_type,
            "engines": sorted(list(self.kernel.engines.keys())),
        }
