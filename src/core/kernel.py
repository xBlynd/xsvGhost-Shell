import os
import platform
import json
from enum import Enum
from typing import Any, Dict, Optional


class EngineState(Enum):
    OFF = "OFF"
    BOOTING = "BOOTING"
    RUNNING = "RUNNING"
    ERROR = "ERROR"


class GhostKernel:
    """GhostCoreEngine + orchestrator.

    Responsible for:
    - Detecting OS / environment
    - Resolving core paths
    - Booting and wiring all Engines
    """

    def __init__(self) -> None:
        self.state = EngineState.OFF
        self.engines: Dict[str, Any] = {}
        self.os_type = platform.system().lower()
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.root_dir, "data")
        self.config_dir = os.path.join(self.data_dir, "config")
        self.vault_dir = os.path.join(self.data_dir, "vault")
        self.logs_dir = os.path.join(self.data_dir, "logs")

        os.makedirs(self.config_dir, exist_ok=True)
        os.makedirs(self.vault_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def boot(self) -> "GhostKernel":
        self.state = EngineState.BOOTING
        print("[GhostCore] Boot sequence starting...")

        # Lazy imports to avoid circulars
        from core.security_engine import SecurityEngine
        from core.heartbeat_engine import HeartbeatEngine
        from core.loader_engine import LoaderEngine
        from core.root_engine import RootEngine
        from core.pulse_engine import PulseEngine
        from core.vault_engine import VaultEngine
        from core.interface_engine import InterfaceEngine
        from core.blackbox_engine import BlackBoxEngine
        from core.ghost_engine import GhostEngine
        from core.sync_engine import SyncEngine

        self.engines["security"] = SecurityEngine(self)
        self.engines["heartbeat"] = HeartbeatEngine(self)
        self.engines["loader"] = LoaderEngine(self)
        self.engines["root"] = RootEngine(self)
        self.engines["pulse"] = PulseEngine(self)
        self.engines["vault"] = VaultEngine(self)
        self.engines["interface"] = InterfaceEngine(self)
        self.engines["blackbox"] = BlackBoxEngine(self)
        self.engines["ghost"] = GhostEngine(self)
        self.engines["sync"] = SyncEngine(self)

        self.state = EngineState.RUNNING
        print("[GhostCore] All engines mounted. System live.\n")
        return self

    def get_engine(self, name: str) -> Optional[Any]:
        return self.engines.get(name)

    # Simple config loader/holder for now
    def load_settings(self) -> Dict[str, Any]:
        path = os.path.join(self.config_dir, "settings.json")
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)


_kernel: Optional[GhostKernel] = None


def initialize() -> GhostKernel:
    global _kernel
    if _kernel is None:
        _kernel = GhostKernel().boot()
    return _kernel
