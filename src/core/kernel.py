"""
Ghost Kernel Phoenix - The Conductor
=====================================
Orchestrates all engine lifecycle, boot sequence, inter-engine communication,
and the main shell loop.

Architecture Notes:
- Engines are loaded in a specific order (dependencies flow downward)
- Each engine receives a kernel reference at init (for inter-engine comms)
- Engine failures are isolated - one bad engine doesn't crash the system
- Future: message bus for async inter-engine communication
"""

import importlib
import sys
import os
import json
import time
from datetime import datetime


class GhostKernel:
    """
    The Ghost Kernel - Central orchestrator for all engines.
    
    This is the ONLY place where engines are aware of each other.
    Engines communicate THROUGH the kernel, never directly importing each other.
    """

    VERSION = "6.5.0-phoenix"
    CODENAME = "Phoenix - Eve Update"

    # === BOOT SEQUENCE ===
    # Order matters! Each engine may depend on engines loaded before it.
    # Format: (name, module_path, class_name)
    BOOT_SEQUENCE = [
        ("ghost_core",  "src.core.ghost_core",        "GhostCoreEngine"),
        ("security",    "src.core.security_engine",    "SecurityEngine"),
        ("heartbeat",   "src.core.heartbeat_engine",   "HeartbeatEngine"),
        ("loader",      "src.core.loader_engine",      "LoaderEngine"),
        ("root",        "src.core.root_engine",         "RootEngine"),
        ("pulse",       "src.core.pulse_engine",        "PulseEngine"),
        ("vault",       "src.core.vault_engine",        "VaultEngine"),
        ("interface",   "src.core.interface_engine",    "InterfaceEngine"),
        ("blackbox",    "src.core.blackbox_engine",     "BlackBoxEngine"),
        ("ghost",       "src.core.ghost_engine",        "GhostEngine"),
        ("sync",        "src.core.sync_engine",         "SyncEngine"),
        # --- Legion is now Phase 1 operational, Eve replaces Cortex ---
        ("legion",      "src.core.legion_engine",       "LegionEngine"),
        ("eve",         "src.core.eve_engine",          "EveEngine"),
    ]

    def __init__(self, root_dir, debug=False):
        self.root_dir = root_dir
        self.debug = debug
        self.engines = {}
        self.commands = {}
        self.aliases = {}
        self.boot_time = None
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.running = False

        # === EVENT BUS (Phase 1: Simple dict-based) ===
        # Future: Replace with async message queue for Legion/Cortex
        self._event_listeners = {}

        # Load aliases from config
        self._load_aliases()

    def _load_aliases(self):
        """Load command aliases from config file."""
        alias_file = os.path.join(self.root_dir, "data", "config", "commands.json")
        if os.path.exists(alias_file):
            try:
                with open(alias_file, 'r') as f:
                    self.aliases = json.load(f)
            except Exception:
                self.aliases = {}

    # =========================================================================
    # BOOT SEQUENCE
    # =========================================================================

    def boot(self):
        """
        Execute the full boot sequence.
        Returns True if minimum viable system is operational.
        """
        self.boot_time = time.time()

        print("\n📌 Connecting to Ghost Kernel Phoenix...")
        print(f"   Version: {self.VERSION} ({self.CODENAME})")
        print(f"   Root: {self.root_dir}")
        print(f"   Session: {self.session_id}")
        print()

        # Phase 1: Load all engines
        loaded = 0
        failed = 0
        critical_ok = True

        for name, module_path, class_name in self.BOOT_SEQUENCE:
            success = self._load_engine(name, module_path, class_name)
            if success:
                loaded += 1
            else:
                failed += 1
                # ghost_core and security are critical - must succeed
                if name in ("ghost_core", "security"):
                    critical_ok = False

        print()
        print(f"   Engines: {loaded} loaded, {failed} failed")

        if not critical_ok:
            print("   [FATAL] Critical engines failed to load. Cannot continue.")
            return False

        # Phase 2: Discover commands
        if "loader" in self.engines and self.engines["loader"]:
            self.commands = self.engines["loader"].discover_commands()
            print(f"   Commands: {len(self.commands)} discovered")

        # Phase 3: Start background services
        if "pulse" in self.engines and self.engines["pulse"]:
            self.engines["pulse"].start()

        # Phase 4: Save session state
        self._save_session()

        elapsed = time.time() - self.boot_time
        print(f"   Boot time: {elapsed:.2f}s")
        print()

        self.running = True
        return True

    def _load_engine(self, name, module_path, class_name):
        """
        Load a single engine with full error isolation.
        Returns True on success, False on failure.
        """
        try:
            module = importlib.import_module(module_path)
            engine_class = getattr(module, class_name)
            engine_instance = engine_class(self)
            self.engines[name] = engine_instance

            if self.debug:
                print(f"   [✓] {name:<12} ({class_name})")
            else:
                print(f"   [✓] {name.capitalize()}")
            return True

        except ImportError as e:
            print(f"   [!] {name.capitalize()} - import error: {e}")
            self.engines[name] = None
            return False

        except Exception as e:
            print(f"   [!] {name.capitalize()} - init error: {e}")
            if self.debug:
                import traceback
                traceback.print_exc()
            self.engines[name] = None
            return False

    # =========================================================================
    # ENGINE ACCESS
    # =========================================================================

    def get_engine(self, name):
        """
        Safely get an engine reference.
        Returns None if engine isn't loaded (callers must handle this).
        """
        return self.engines.get(name)

    def engine_available(self, name):
        """Check if an engine is loaded and operational."""
        return name in self.engines and self.engines[name] is not None

    # =========================================================================
    # EVENT BUS (Simple Phase 1 Implementation)
    # =========================================================================

    def on(self, event_name, callback):
        """Register an event listener."""
        if event_name not in self._event_listeners:
            self._event_listeners[event_name] = []
        self._event_listeners[event_name].append(callback)

    def emit(self, event_name, data=None):
        """Emit an event to all registered listeners."""
        if event_name in self._event_listeners:
            for callback in self._event_listeners[event_name]:
                try:
                    callback(data)
                except Exception as e:
                    if self.debug:
                        print(f"[EventBus] Error in {event_name} handler: {e}")

    # =========================================================================
    # COMMAND RESOLUTION & EXECUTION
    # =========================================================================

    def resolve_and_execute(self, raw_input):
        """
        The Resolution Chain:
        1. Ghost Command (cmd_*.py) - highest priority
        2. Alias (commands.json) - magic launcher
        3. Host OS Passthrough - fallback
        """
        raw_input = raw_input.strip()
        if not raw_input:
            return

        parts = raw_input.split(None, 1)
        cmd_name = parts[0].lower()
        args_str = parts[1] if len(parts) > 1 else ""

        # 1. Check Ghost Commands
        if cmd_name in self.commands:
            return self._execute_ghost_command(cmd_name, args_str)

        # 2. Check Aliases
        if cmd_name in self.aliases:
            alias_cmd = self.aliases[cmd_name]
            if "{target}" in alias_cmd and args_str:
                alias_cmd = alias_cmd.replace("{target}", args_str)
            return self._execute_passthrough(alias_cmd)

        # 3. Host OS Passthrough
        return self._execute_passthrough(raw_input)

    def _execute_ghost_command(self, cmd_name, args_str):
        """Execute a Ghost Shell command with permission checking."""
        cmd_module = self.commands[cmd_name]

        # Check permissions
        required_role = getattr(cmd_module, 'REQUIRED_ROLE', None)
        if required_role and self.engine_available("security"):
            sec = self.engines["security"]
            if not sec.has_permission(required_role):
                print(f"[!] Access Denied. Required role: {required_role}")
                return

        # Execute
        try:
            result = cmd_module.execute(self, args_str)
            if result:
                print(result)
        except Exception as e:
            print(f"[!] Command '{cmd_name}' error: {e}")
            if self.debug:
                import traceback
                traceback.print_exc()

    def _execute_passthrough(self, cmd):
        """Pass command to host OS shell."""
        if self.engine_available("root"):
            stdout, stderr = self.engines["root"].exec_silent(cmd)
            if stdout:
                print(stdout.rstrip())
            if stderr:
                print(stderr.rstrip())
        else:
            # Fallback if RootEngine unavailable
            import subprocess
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.stdout:
                    print(result.stdout.rstrip())
                if result.stderr:
                    print(result.stderr.rstrip())
            except Exception as e:
                print(f"[!] Execution error: {e}")

    # =========================================================================
    # SHELL LOOP
    # =========================================================================

    def run_shell(self):
        """Main interactive shell loop."""
        # Show banner
        if self.engine_available("interface"):
            role = None
            if self.engine_available("security"):
                role = self.engines["security"].current_role
            banner = self.engines["interface"].get_banner(role)
            print(banner)

        # Get prompt
        prompt = self._get_prompt()

        # Main loop
        while self.running:
            try:
                user_input = input(prompt)
                if not user_input.strip():
                    continue

                # Special built-in: exit/quit
                if user_input.strip().lower() in ("exit", "quit"):
                    print("[Ghost] Shutting down...")
                    self.running = False
                    break

                self.resolve_and_execute(user_input)

            except KeyboardInterrupt:
                print()  # Newline after ^C
                continue
            except EOFError:
                self.running = False
                break

    def _get_prompt(self):
        """Generate the shell prompt based on current state."""
        role_tag = ""
        if self.engine_available("security"):
            role = self.engines["security"].current_role
            if role == "GOD":
                role_tag = "⚡"
            elif role == "ADMIN":
                role_tag = "◆"
            else:
                role_tag = "○"

        return f"\n{role_tag}xsv> "

    # =========================================================================
    # SESSION MANAGEMENT
    # =========================================================================

    def _save_session(self):
        """Persist session state for crash recovery and audit."""
        session_file = os.path.join(self.root_dir, "data", "session", "current.json")
        os.makedirs(os.path.dirname(session_file), exist_ok=True)

        session_data = {
            "session_id": self.session_id,
            "boot_time": self.boot_time,
            "version": self.VERSION,
            "engines_loaded": [k for k, v in self.engines.items() if v is not None],
            "engines_failed": [k for k, v in self.engines.items() if v is None],
            "commands_loaded": list(self.commands.keys()),
            "os": os.name,
            "python": sys.version,
        }

        try:
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
        except Exception:
            pass  # Session save is not critical

    # =========================================================================
    # SHUTDOWN
    # =========================================================================

    def shutdown(self):
        """Graceful shutdown - cleanup in reverse boot order."""
        self.running = False
        self.emit("shutdown")

        # Run ghost cleanup (stealth engine)
        if self.engine_available("ghost"):
            try:
                self.engines["ghost"].cleanup()
            except Exception:
                pass

        # Stop pulse (background tasks)
        if self.engine_available("pulse"):
            try:
                self.engines["pulse"].stop()
            except Exception:
                pass

        # Save final session state
        self._save_session()
