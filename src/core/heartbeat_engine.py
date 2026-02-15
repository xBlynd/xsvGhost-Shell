"""
Engine 11: Heartbeat Engine - The Immune System
=================================================
Memory usage, thread health, engine status, self-diagnostics.

Compartmentalization:
- Read-only monitoring
- Can trigger alerts but does NOT directly fix issues
"""

import threading
import sys
import os
import time


class HeartbeatEngine:
    """The Immune System - health monitoring."""

    ENGINE_NAME = "heartbeat"
    ENGINE_VERSION = "1.0.0"

    def __init__(self, kernel):
        self.kernel = kernel
        self.boot_time = time.time()

    def check_health(self):
        """Full system health check."""
        return {
            "uptime_seconds": round(time.time() - self.boot_time, 1),
            "threads": threading.active_count(),
            "thread_names": [t.name for t in threading.enumerate()],
            "memory": self._get_memory(),
            "engines": self._check_engines(),
            "python": sys.version,
            "status": self._overall_status(),
        }

    def _get_memory(self):
        """Get memory usage. Uses psutil if available, falls back to basic."""
        try:
            import psutil
            proc = psutil.Process()
            mem = proc.memory_info()
            return {
                "rss_mb": round(mem.rss / (1024 * 1024), 2),
                "vms_mb": round(mem.vms / (1024 * 1024), 2),
                "source": "psutil",
            }
        except ImportError:
            # Fallback: read from /proc on Linux
            try:
                with open(f"/proc/{os.getpid()}/status", 'r') as f:
                    for line in f:
                        if line.startswith("VmRSS:"):
                            kb = int(line.split()[1])
                            return {
                                "rss_mb": round(kb / 1024, 2),
                                "source": "proc",
                            }
            except Exception:
                pass

            return {"rss_mb": "unknown", "source": "unavailable"}

    def _check_engines(self):
        """Check which engines are loaded vs failed."""
        loaded = []
        failed = []
        for name, engine in self.kernel.engines.items():
            if engine is not None:
                loaded.append(name)
            else:
                failed.append(name)
        return {
            "loaded": loaded,
            "failed": failed,
            "total": len(self.kernel.engines),
        }

    def _overall_status(self):
        """Determine overall system health."""
        engines = self._check_engines()

        if len(engines["failed"]) == 0:
            return "HEALTHY"
        elif any(e in engines["failed"] for e in ["ghost_core", "security"]):
            return "CRITICAL"
        elif len(engines["failed"]) > 3:
            return "DEGRADED"
        else:
            return "OPERATIONAL"
