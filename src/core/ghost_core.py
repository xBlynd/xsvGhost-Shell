"""
Engine 01: Ghost Core - The Brain
==================================
System state, environmental awareness, node identity.
This is the FIRST engine to boot and establishes the foundation
everything else builds on.

Compartmentalization:
- MUST NOT perform authentication (SecurityEngine)
- MUST NOT load commands (LoaderEngine)
- ONLY detects environment and sets up paths
"""

import os
import sys
import json
import uuid
import platform
from datetime import datetime


class GhostCoreEngine:
    """
    The Brain of Ghost Shell.
    Detects OS, calculates ROOT_DIR, manages node identity and session state.
    """

    ENGINE_NAME = "ghost_core"
    ENGINE_VERSION = "1.0.0"

    def __init__(self, kernel):
        self.kernel = kernel

        # === CRITICAL: Initialize ALL attributes before any method calls ===
        self.root_dir = kernel.root_dir
        self.node_type = "MASTER"      # MASTER | LEGIONNAIRE | HIVE_MIND
        self.node_id = None
        self.os_type = None
        self.os_version = None
        self.hostname = None
        self.is_portable = False       # Running from USB?
        self.python_version = None
        self.boot_timestamp = datetime.now().isoformat()

        # === Detect environment ===
        self._detect_os()
        self._detect_portability()
        self._load_or_generate_node_id()
        self._ensure_data_directories()

    def _detect_os(self):
        """Detect the host operating system and capabilities."""
        self.os_type = platform.system().upper()  # WINDOWS, LINUX, DARWIN
        self.os_version = platform.version()
        self.hostname = platform.node()
        self.python_version = platform.python_version()

        # Normalize for our purposes
        if self.os_type == "DARWIN":
            self.os_type = "MACOS"

        # Android detection (runs as Linux but has different paths)
        if self.os_type == "LINUX":
            if os.path.exists("/sdcard") or "ANDROID" in os.environ.get("PREFIX", "").upper():
                self.os_type = "ANDROID"

    def _detect_portability(self):
        """Determine if we're running from removable media."""
        if self.os_type == "WINDOWS":
            try:
                import ctypes
                drive = os.path.splitdrive(self.root_dir)[0] + "\\"
                drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive)
                self.is_portable = (drive_type == 2)  # DRIVE_REMOVABLE
            except Exception:
                self.is_portable = False
        else:
            # On Linux/Mac, check if we're on a mount point typical of USB
            self.is_portable = any(
                self.root_dir.startswith(p)
                for p in ["/media/", "/mnt/usb", "/run/media/"]
            )

    def _load_or_generate_node_id(self):
        """
        Load or generate a unique node identity.
        This ID persists across sessions and identifies this Ghost Shell instance
        in Legion mode (multi-device mesh).
        """
        node_file = os.path.join(self.root_dir, "data", "session", "node.json")
        os.makedirs(os.path.dirname(node_file), exist_ok=True)

        if os.path.exists(node_file):
            try:
                with open(node_file, 'r') as f:
                    node_data = json.load(f)
                    self.node_id = node_data.get("node_id")
                    self.node_type = node_data.get("node_type", self.node_type)
            except Exception:
                pass

        if not self.node_id:
            # Generate new node identity
            self.node_id = f"ghost-{uuid.uuid4().hex[:12]}"
            node_data = {
                "node_id": self.node_id,
                "node_type": self.node_type,
                "created": self.boot_timestamp,
                "hostname": self.hostname,
                "os": self.os_type,
            }
            try:
                with open(node_file, 'w') as f:
                    json.dump(node_data, f, indent=2)
            except Exception:
                pass

    def _ensure_data_directories(self):
        """Create required data directories if they don't exist."""
        dirs = [
            "data/keys",
            "data/vault/journal",
            "data/vault/todos",
            "data/vault/encrypted",
            "data/config",
            "data/session",
            "data/queue",
            "data/legion",
        ]
        for d in dirs:
            full_path = os.path.join(self.root_dir, d)
            os.makedirs(full_path, exist_ok=True)

    # =========================================================================
    # PUBLIC API
    # =========================================================================

    def get_path(self, *parts):
        """
        Resolve a path relative to ROOT_DIR.
        Usage: core.get_path("data", "vault", "journal")
        """
        return os.path.join(self.root_dir, *parts)

    def get_state(self):
        """Return current system state as a dict."""
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "os": self.os_type,
            "os_version": self.os_version,
            "hostname": self.hostname,
            "python": self.python_version,
            "portable": self.is_portable,
            "root_dir": self.root_dir,
            "boot_time": self.boot_timestamp,
            "version": self.ENGINE_VERSION,
        }

    def set_node_type(self, node_type):
        """Update node type (MASTER, LEGIONNAIRE, HIVE_MIND)."""
        valid_types = ("MASTER", "LEGIONNAIRE", "HIVE_MIND")
        if node_type.upper() in valid_types:
            self.node_type = node_type.upper()
            # Persist
            self._load_or_generate_node_id()
