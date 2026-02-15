"""
Ghost Kernel - Engine Orchestrator
Manages engine lifecycle, dependencies, and failure recovery.
"""
import sys
import importlib
from pathlib import Path
from queue import Queue
from threading import Lock, Event
from enum import Enum
import json

ROOT = Path(__file__).parent.parent.parent

class EngineState(Enum):
    UNLOADED = "unloaded"
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    DEGRADED = "degraded"
    FAILED = "failed"
    DISABLED = "disabled"
    SHUTDOWN = "shutdown"

class CriticalEngineFailure(Exception):
    """Raised when a critical engine fails - shell cannot continue"""
    pass

class EngineMessenger:
    """Thread-safe message passing between engines"""
    def __init__(self):
        self.queues = {}
        self.lock = Lock()
    
    def register(self, engine_name):
        with self.lock:
            self.queues[engine_name] = Queue()
    
    def send(self, target_engine, message):
        with self.lock:
            if target_engine in self.queues:
                self.queues[target_engine].put(message)
    
    def receive(self, engine_name, timeout=0.1):
        try:
            return self.queues[engine_name].get(timeout=timeout)
        except:
            return None

class EngineWrapper:
    """Wraps an engine with state tracking and health monitoring"""
    def __init__(self, name, module_path, class_name, critical=True, enabled=True):
        self.name = name
        self.module_path = module_path
        self.class_name = class_name
        self.critical = critical
        self.enabled = enabled
        self.state = EngineState.DISABLED if not enabled else EngineState.UNLOADED
        self.instance = None
        self.restart_attempts = 0
        self.max_restarts = 3
        self.errors = []
    
    def load(self):
        """Import and initialize the engine"""
        if not self.enabled:
            self.state = EngineState.DISABLED
            return False
        
        try:
            self.state = EngineState.INITIALIZING
            module = importlib.import_module(self.module_path)
            engine_class = getattr(module, self.class_name)
            
            self.instance = engine_class()
            if hasattr(self.instance, 'initialize'):
                self.instance.initialize()
            
            self.state = EngineState.RUNNING
            return True
        
        except Exception as e:
            self.errors.append(str(e))
            self.state = EngineState.FAILED
            if self.critical:
                raise CriticalEngineFailure(f"{self.name} failed: {e}")
            return False
    
    def restart(self):
        """Attempt to restart a failed engine"""
        if self.restart_attempts >= self.max_restarts:
            self.state = EngineState.FAILED
            return False
        
        self.restart_attempts += 1
        print(f"⚠ Restarting {self.name} (attempt {self.restart_attempts}/{self.max_restarts})")
        return self.load()
    
    def shutdown(self):
        """Gracefully shutdown the engine"""
        if self.instance and hasattr(self.instance, 'shutdown'):
            try:
                self.instance.shutdown()
            except Exception as e:
                print(f"⚠ Error shutting down {self.name}: {e}")
        self.state = EngineState.SHUTDOWN

class GhostKernel:
    """
    The Ghost Shell Kernel
    Manages engine boot sequence, health monitoring, and graceful shutdown.
    
    BOOT SEQUENCE - ALIGNED WITH GHOST SYSTEM ATLAS
    The 11 Canonical Engines (no hallucinations)
    """
    
    # Boot sequence - ORDER MATTERS
    # Format: (name, module_path, class_name, is_critical, enabled)
    BOOT_SEQUENCE = [
        # PHASE 1: Core Brain (MUST boot first)
        ('ghost_core', 'src.core.ghost_core', 'GhostCoreEngine', True, True),
        
        # PHASE 2: Security & Data (Critical foundation)
        ('security', 'src.core.security_engine', 'SecurityEngine', True, True),
        ('vault', 'src.core.vault_engine', 'VaultEngine', True, True),
        
        # PHASE 3: System Control (God Mode)
        ('root', 'src.core.root_engine', 'RootEngine', True, True),
        
        # PHASE 4: Time & Health (Consciousness)
        ('pulse', 'src.core.pulse_engine', 'PulseEngine', False, True),
        ('heartbeat', 'src.core.heartbeat_engine', 'HeartbeatEngine', False, True),
        
        # PHASE 5: Interface & Loading (User-facing)
        ('loader', 'src.core.loader_engine', 'LoaderEngine', False, False),  # Disabled (WIP)
        ('interface', 'src.core.interface_engine', 'InterfaceEngine', False, False),  # Disabled (WIP)
        
        # PHASE 6: Advanced Operations (Not built yet)
        ('sync', 'src.core.sync_engine', 'SyncEngine', False, False),  # Disabled
        ('ghost', 'src.core.ghost_engine', 'GhostEngine', False, False),  # Disabled (stealth)
        ('blackbox', 'src.core.blackbox_engine', 'BlackBoxEngine', False, False),  # Disabled (network)
    ]
    
    def __init__(self):
        self.engines = {}
        self.messenger = EngineMessenger()
        self.shutdown_event = Event()
        self.degraded_mode = False
        self.config = self.load_engine_config()
    
    def load_engine_config(self):
        """Load engine enable/disable config"""
        config_file = ROOT / 'data' / 'config' / 'engines.json'
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def boot(self):
        """Initialize all engines in boot sequence"""
        print("👻 Ghost Shell Kernel Booting...\n")
        
        for name, module_path, class_name, critical, enabled in self.BOOT_SEQUENCE:
            # Check config override
            if name in self.config:
                enabled = self.config[name].get('enabled', enabled)
            
            wrapper = EngineWrapper(name, module_path, class_name, critical, enabled)
            self.messenger.register(name)
            
            if not enabled:
                self.engines[name] = wrapper
                print(f"○ {name.upper()}: disabled (config)")
                continue
            
            try:
                if wrapper.load():
                    self.engines[name] = wrapper
                    print(f"✓ {name.upper()}: {wrapper.state.value}")
                else:
                    self.engines[name] = wrapper
                    if critical:
                        raise CriticalEngineFailure(f"{name} is critical and failed")
                    self.degraded_mode = True
                    print(f"⚠ {name.upper()}: FAILED (non-critical)")
            
            except CriticalEngineFailure as e:
                print(f"\n❌ BOOT FAILURE: {e}")
                self.emergency_shutdown()
                raise
        
        # Set kernel reference in heartbeat engine
        if 'heartbeat' in self.engines and self.engines['heartbeat'].instance:
            self.engines['heartbeat'].instance.kernel = self
        
        if self.degraded_mode:
            print("\n⚠ Ghost Shell running in DEGRADED mode")
        else:
            print("\n✓ Ghost Shell fully operational")
        
        return True
    
    def get_engine(self, name):
        """Get engine instance by name"""
        wrapper = self.engines.get(name)
        return wrapper.instance if wrapper and wrapper.state == EngineState.RUNNING else None
    
    def enable_engine(self, name):
        """Enable and start an engine"""
        wrapper = self.engines.get(name)
        if wrapper and wrapper.state == EngineState.DISABLED:
            wrapper.enabled = True
            if wrapper.load():
                print(f"✓ {name} enabled")
                return True
        return False
    
    def disable_engine(self, name):
        """Disable and stop an engine"""
        wrapper = self.engines.get(name)
        if wrapper and wrapper.state == EngineState.RUNNING:
            wrapper.shutdown()
            wrapper.enabled = False
            wrapper.state = EngineState.DISABLED
            print(f"○ {name} disabled")
            return True
        return False
    
    def monitor_health(self):
        """Check health of all engines"""
        results = {}
        for name, wrapper in self.engines.items():
            results[name] = {
                'state': wrapper.state.value,
                'restarts': wrapper.restart_attempts,
                'errors': len(wrapper.errors),
                'enabled': wrapper.enabled
            }
        return results
    
    def emergency_shutdown(self):
        """Immediate shutdown on critical failure"""
        print("\n⚠ EMERGENCY SHUTDOWN")
        self.shutdown()
    
    def shutdown(self):
        """Graceful shutdown - REVERSE boot order"""
        print("\n👻 Ghost Shell Kernel Shutting Down...")
        self.shutdown_event.set()
        
        # Shutdown in reverse order
        for name, _, _, _, _ in reversed(self.BOOT_SEQUENCE):
            if name in self.engines:
                wrapper = self.engines[name]
                if wrapper.state == EngineState.RUNNING:
                    print(f"  Stopping {name}...")
                    wrapper.shutdown()
        
        print("✓ Ghost Shell stopped cleanly")

# Global kernel instance
kernel = None

def initialize():
    """Initialize the Ghost Kernel"""
    global kernel
    kernel = GhostKernel()
    return kernel.boot()

def get_kernel():
    """Get the running kernel instance"""
    return kernel
