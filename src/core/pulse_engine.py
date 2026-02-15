"""
Engine 06: Pulse Engine - The Heartbeat
=========================================
Background reminders, scheduled tasks, time-based triggers.
Uses daemon threads so it NEVER blocks the main shell or causes lag.

Compartmentalization:
- Runs in isolated daemon thread
- MUST NOT perform blocking I/O
- Communicates via kernel event bus
"""

import threading
import time
from datetime import datetime


class PulseEngine:
    """The Heartbeat - time and scheduling."""

    ENGINE_NAME = "pulse"
    ENGINE_VERSION = "1.0.0"

    def __init__(self, kernel):
        self.kernel = kernel
        self.running = False
        self._thread = None
        self._tasks = []  # List of (interval_seconds, callback, last_run, name)
        self._lock = threading.Lock()

        # Register built-in periodic tasks
        self.register_task("session_autosave", 300, self._autosave_session)  # Every 5 min

    def start(self):
        """Start the pulse loop in a daemon thread."""
        if self.running:
            return

        self.running = True
        self._thread = threading.Thread(
            target=self._pulse_loop,
            daemon=True,  # CRITICAL: daemon=True means no lag, clean shutdown
            name="GhostPulse"
        )
        self._thread.start()

    def stop(self):
        """Stop the pulse loop."""
        self.running = False

    def register_task(self, name, interval_seconds, callback):
        """Register a periodic task."""
        with self._lock:
            self._tasks.append({
                "name": name,
                "interval": interval_seconds,
                "callback": callback,
                "last_run": 0,
            })

    def _pulse_loop(self):
        """Main pulse loop - runs in background thread."""
        while self.running:
            now = time.time()

            with self._lock:
                for task in self._tasks:
                    if now - task["last_run"] >= task["interval"]:
                        try:
                            task["callback"]()
                            task["last_run"] = now
                        except Exception:
                            pass  # Never crash the pulse loop

            # Sleep in small increments so we can stop quickly
            for _ in range(10):
                if not self.running:
                    break
                time.sleep(1)

    def _autosave_session(self):
        """Periodic session state save."""
        try:
            self.kernel._save_session()
        except Exception:
            pass

    def get_status(self):
        """Return pulse engine status."""
        with self._lock:
            return {
                "running": self.running,
                "thread_alive": self._thread.is_alive() if self._thread else False,
                "registered_tasks": len(self._tasks),
                "tasks": [
                    {
                        "name": t["name"],
                        "interval_s": t["interval"],
                        "last_run": datetime.fromtimestamp(t["last_run"]).isoformat() if t["last_run"] else "never",
                    }
                    for t in self._tasks
                ],
            }
