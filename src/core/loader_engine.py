"""
Loader Engine - The Nervous System
Dynamic command discovery and hot reload
"""

import os
import importlib
import importlib.util
from pathlib import Path

class LoaderEngine:
    """
    Discovers and loads commands dynamically.
    Supports hot reload for live development.
    """
    
    def __init__(self, kernel):
        self.kernel = kernel
        self.name = "loader"
        self.commands = {}
        self.command_modules = {}
        
        # Get commands directory
        core = kernel.engines.get('ghost_core')
        if core:
            self.commands_dir = core.get_path("src", "commands")
        else:
            self.commands_dir = Path(__file__).parent.parent / "commands"
        
        # Discover commands
        self._discover_commands()
    
    def _discover_commands(self):
        """
        Scan commands directory for cmd_*.py files.
        Drop-in command system - just add a file.
        """
        if not self.commands_dir.exists():
            self.commands_dir.mkdir(parents=True, exist_ok=True)
            return
        
        for file in self.commands_dir.glob("cmd_*.py"):
            cmd_name = file.stem[4:]  # Remove 'cmd_' prefix
            
            try:
                # Import module
                spec = importlib.util.spec_from_file_location(
                    f"commands.{file.stem}",
                    file
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Store module and command
                self.command_modules[cmd_name] = module
                self.commands[cmd_name] = module
                
            except Exception as e:
                print(f"   ⚠ Failed to load {cmd_name}: {e}")
        
        # Register with kernel
        self.kernel.commands = self.commands
    
    def reload_command(self, cmd_name):
        """
        Hot reload a command.
        Edit code without restarting shell.
        """
        if cmd_name not in self.command_modules:
            return False, "Command not found"
        
        try:
            module = self.command_modules[cmd_name]
            importlib.reload(module)
            self.commands[cmd_name] = module
            return True, f"Reloaded {cmd_name}"
        except Exception as e:
            return False, f"Reload failed: {e}"
    
    def get_command_help(self, cmd_name):
        """Get help text for command"""
        if cmd_name not in self.commands:
            return None
        
        module = self.commands[cmd_name]
        
        # Try to get HELP attribute
        if hasattr(module, 'HELP'):
            return module.HELP
        
        # Fallback to docstring
        if hasattr(module, 'execute'):
            return module.execute.__doc__ or "No help available"
        
        return "No help available"
    
    def list_commands(self):
        """Get list of available commands"""
        return sorted(self.commands.keys())
