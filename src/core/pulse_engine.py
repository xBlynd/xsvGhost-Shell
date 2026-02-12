import threading
import time
from typing import Any, Callable


class PulseEngine:
    """The Timekeeper: simple heartbeat loop + scheduling hooks."""

    def __init__(self, kernel: Any) -> None:
        self.kernel = kernel
        self._stop = False
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self) -> None:
        self._thread.start()

    def _run(self) -> None:
        while not self._stop:
            time.sleep(1.0)

    def stop(self) -> None:
        self._stop = True
