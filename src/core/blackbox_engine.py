from typing import Any


class BlackBoxEngine:
    """The Shadow Network.

    Phoenix v0: focused on ping/jitter and CSV logging hooks.
    """

    def __init__(self, kernel: Any) -> None:
        self.kernel = kernel

