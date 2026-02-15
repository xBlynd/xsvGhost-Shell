"""
Engine 08: Sync Engine - The Bridge
=====================================
USB-to-local file sync, git integration, store-and-forward.

Compartmentalization:
- Only activates if running from removable media
- MUST NOT overwrite user data without confirmation
"""

import os
import json
import shutil
from datetime import datetime


class SyncEngine:
    """The Bridge - data synchronization and transport."""

    ENGINE_NAME = "sync"
    ENGINE_VERSION = "1.0.0"

    def __init__(self, kernel):
        self.kernel = kernel
        self.root_dir = kernel.root_dir
        self.queue_dir = os.path.join(self.root_dir, "data", "queue")
        os.makedirs(self.queue_dir, exist_ok=True)

    def is_running_from_usb(self):
        """Detect if running from removable media."""
        core = self.kernel.get_engine("ghost_core")
        if core:
            return core.is_portable
        return False

    def queue_operation(self, operation, data):
        """
        Store-and-forward: queue an operation for later sync.
        Used when offline or when target is unreachable.
        """
        queue_file = os.path.join(self.queue_dir, "pending.json")

        queue = []
        if os.path.exists(queue_file):
            try:
                with open(queue_file, 'r') as f:
                    queue = json.load(f)
            except Exception:
                queue = []

        queue.append({
            "operation": operation,
            "data": data,
            "queued_at": datetime.now().isoformat(),
            "status": "pending",
        })

        with open(queue_file, 'w') as f:
            json.dump(queue, f, indent=2)

        return len(queue)

    def get_queue(self):
        """Get pending sync operations."""
        queue_file = os.path.join(self.queue_dir, "pending.json")
        if os.path.exists(queue_file):
            try:
                with open(queue_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def flush_queue(self):
        """Process all pending sync operations."""
        # Future: implement actual sync logic
        queue_file = os.path.join(self.queue_dir, "pending.json")
        if os.path.exists(queue_file):
            os.remove(queue_file)
        return {"flushed": True}

    def get_status(self):
        """Return sync engine status."""
        return {
            "portable": self.is_running_from_usb(),
            "pending_operations": len(self.get_queue()),
        }
