from typing import Any


class SecurityEngine:
    """The Gatekeeper.

    Dev-pass implementation: structure only, no real crypto yet.
    """

    def __init__(self, kernel: Any) -> None:
        self.kernel = kernel
        self.authenticated = True  # Dev mode
