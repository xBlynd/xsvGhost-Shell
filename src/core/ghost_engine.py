from typing import Any


class GhostEngine:
    """The Phantom.

    Phoenix v0: stealth hooks only (no-op with logging).
    """

    def __init__(self, kernel: Any) -> None:
        self.kernel = kernel

