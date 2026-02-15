"""
Ghost Shell Phoenix - Kernel
The Orchestrator - Coordinates all 11 engines
"""

import os
import sys
import importlib
from datetime import datetime

class GhostKernel:
    """
    The central orchestrator for Ghost Shell.
    Loads engines, manages lifecycle, provides inter-engine communication.
    """
    
    # Boot sequence - order matters for dependencies
    BOOT_SEQUENCE = [
        ("ghost_core", "core.ghost_core", "GhostCoreEngine"),
        ("security", "core.security_engine", "SecurityEngine"),
        ("heartbeat", "core.heartbeat_engine", "HeartbeatEngine"),
        ("loader", "core.loader_engine", "LoaderEngine"),
        ("root", "core.root_engine", "RootEngine"),
        ("pulse", "core.pulse_engine", "PulseEngine"),
        ("vault", "core.vault_engine", "VaultEngine"),
        ("interface", "core.interface_engine", "InterfaceEngine"),
        ("blackbox", "core.blackbox_engine", "BlackBoxEngine"),
        ("ghost", "core.ghost_engine", "GhostEngine"),
        ("sync", "core.sync_engine", "SyncEngine"),
    ]
    
    def __init__(self):
        self.engines = {}
        self.commands = {}
        self.running = False
        self.message_bus = MessageBus()
        
    def boot(self):
        """Boot sequence - load all engines"""
        print("🔌 Ghost Shell Phoenix - Booting...")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("─" * 50)
        
        for name, module_path, class_name in self.BOOT_SEQUENCE:
            try:
                module = importlib.import_module(module_path)
                engine_class = getattr(module, class_name)
                self.engines[name] = engine_class(self)
                print(f"   ✓ {name.capitalize()}")
            except Exception as e:
                print(f"   ✗ {name.capitalize()}: {e}")
                self.engines[name] = None  # Mark as unavailable but continue
        
        print("─" * 50)
        
        # Let engines finish initialization
        for name, engine in self.engines.items():
            if engine and hasattr(engine, 'post_boot'):
                try:
                    engine.post_boot()
                except Exception as e:
                    print(f"   ⚠ {name} post-boot warning: {e}")
        
        self.running = True
        
    def run(self):
        """Main shell loop"""
        if not self.running:
            print("[Error] Kernel not booted")
            return
            
        # Show interface
        if self.engines.get('interface'):
            self.engines['interface'].show_banner()
        
        # Enter shell loop
        if self.engines.get('loader'):
            # Use loader's shell if available
            shell_cmd = self.commands.get('shell')
            if shell_cmd:
                shell_cmd.execute(self, [])
            else:
                self._basic_shell()
        else:
            self._basic_shell()
    
    def _basic_shell(self):
        """Fallback basic shell if loader fails"""
        print("\n[Fallback Shell - Loader unavailable]")
        while self.running:
            try:
                cmd = input("ghost> ").strip()
                if cmd in ['exit', 'quit']:
                    break
                elif cmd == 'status':
                    print(f"Engines loaded: {len([e for e in self.engines.values() if e])}/11")
                elif cmd:
                    print(f"Unknown command: {cmd}")
            except (EOFError, KeyboardInterrupt):
                break
        
        self.shutdown()
    
    def shutdown(self):
        """Clean shutdown"""
        print("\n[Ghost] Initiating shutdown...")
        
        # Let ghost engine clean up
        if self.engines.get('ghost'):
            try:
                self.engines['ghost'].cleanup()
            except Exception as e:
                print(f"   ⚠ Cleanup warning: {e}")
        
        self.running = False
        print("[Ghost] Disconnected.")


class MessageBus:
    """
    Simple message bus for inter-engine communication.
    Engines should use this instead of direct coupling.
    """
    
    def __init__(self):
        self.subscribers = {}
        
    def subscribe(self, channel, callback):
        """Subscribe to a message channel"""
        if channel not in self.subscribers:
            self.subscribers[channel] = []
        self.subscribers[channel].append(callback)
    
    def publish(self, channel, message):
        """Publish message to channel"""
        if channel in self.subscribers:
            for callback in self.subscribers[channel]:
                try:
                    callback(message)
                except Exception as e:
                    print(f"[MessageBus] Error in subscriber: {e}")
    
    def send(self, target_engine, method, *args, **kwargs):
        """
        Direct engine communication helper.
        Returns None if engine unavailable.
        """
        # This will be populated by kernel
        return None
