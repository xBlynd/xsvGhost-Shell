import importlib
import os
from types import ModuleType
from typing import Any, Dict, Optional


class LoaderEngine:
    """The Nervous System: command discovery and routing."""

    def __init__(self, kernel: Any) -> None:
        self.kernel = kernel
        self._commands: Dict[str, ModuleType] = {}
        self._scan_commands()

    def _scan_commands(self) -> None:
        commands_dir = os.path.join(self.kernel.src_dir, "commands")
        if not os.path.isdir(commands_dir):
            return
        for filename in os.listdir(commands_dir):
            if not filename.startswith("cmd_") or not filename.endswith(".py"):
                continue
            mod_name = filename[:-3]
            module_path = f"commands.{mod_name}"
            module = importlib.import_module(module_path)
            manifest = getattr(module, "MANIFEST", None)
            if not isinstance(manifest, dict) or "name" not in manifest:
                continue
            self._commands[manifest["name"]] = module

    def list_commands(self) -> Dict[str, ModuleType]:
        return dict(self._commands)

    def get_command(self, name: str) -> Optional[ModuleType]:
        return self._commands.get(name)
