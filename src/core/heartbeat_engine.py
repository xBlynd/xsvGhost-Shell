from typing import Any


class HeartbeatEngine:
    """The Immune System: simple status tracker for now."""

    def __init__(self, kernel: Any) -> None:
        self.kernel = kernel
        self.beats = 0
