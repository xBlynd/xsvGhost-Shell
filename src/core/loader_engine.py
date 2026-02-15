"""
Engine 10: Loader Engine - The Nervous System
================================================
Scans src/commands/ for cmd_*.py files, dynamic import, hot reload.

The Drop-In Pattern:
- Want a new command? Just create src/commands/cmd_whatever.py
- It's automatically discovered on next boot
- Hot reload: edit the file and run `reload whatever` without restarting

Compartmentalization:
- ONLY manages command loading/reloading
- Does NOT execute commands (kernel does that)
"""

import importlib
import os
import sys


class LoaderEngine:
    """The Nervous System - dynamic command management."""

    ENGINE_NAME = "loader"
    ENGINE_VERSION = "1.0.0"

    def __init__(self, kernel):
        self.kernel = kernel
        self.root_dir = kernel.root_dir
        self.commands_dir = os.path.join(self.root_dir, "src", "commands")
        self._loaded_modules = {}

    def discover_commands(self):
        """
        Scan src/commands/ for cmd_*.py files and import them.
        Returns dict of {command_name: module}.
        """
        commands = {}

        if not os.path.exists(self.commands_dir):
            return commands

        for filename in os.listdir(self.commands_dir):
            if filename.startswith("cmd_") and filename.endswith(".py"):
                cmd_name = filename[4:-3]  # Remove 'cmd_' prefix and '.py'

                try:
                    module_path = f"src.commands.{filename[:-3]}"
                    module = importlib.import_module(module_path)
                    commands[cmd_name] = module
                    self._loaded_modules[cmd_name] = module
                except Exception as e:
                    if self.kernel.debug:
                        print(f"   [!] Failed to load command '{cmd_name}': {e}")

        return commands

    def reload_command(self, cmd_name):
        """
        Hot reload a single command module.
        Edit cmd_ping.py and run `reload ping` - no restart needed!
        """
        if cmd_name not in self._loaded_modules:
            return False, f"Command '{cmd_name}' not loaded"

        try:
            module = self._loaded_modules[cmd_name]
            importlib.reload(module)
            self.kernel.commands[cmd_name] = module
            return True, f"Command '{cmd_name}' reloaded"
        except Exception as e:
            return False, f"Reload failed: {e}"

    def reload_all(self):
        """Reload all loaded commands."""
        results = {}
        for cmd_name in list(self._loaded_modules.keys()):
            success, msg = self.reload_command(cmd_name)
            results[cmd_name] = {"success": success, "message": msg}
        return results

    def get_command_info(self, cmd_name):
        """Get metadata about a command."""
        if cmd_name not in self._loaded_modules:
            return None

        module = self._loaded_modules[cmd_name]
        return {
            "name": cmd_name,
            "description": getattr(module, 'DESCRIPTION', 'No description'),
            "required_role": getattr(module, 'REQUIRED_ROLE', None),
            "usage": getattr(module, 'USAGE', None),
            "file": getattr(module, '__file__', 'unknown'),
        }

    def list_commands(self):
        """List all discovered commands with metadata."""
        return {
            name: self.get_command_info(name)
            for name in sorted(self._loaded_modules.keys())
        }
