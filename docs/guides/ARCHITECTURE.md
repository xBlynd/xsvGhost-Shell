# Ghost Shell OS - System Architecture

## Overview

Ghost Shell is a portable, command-driven operating system shell designed for advanced system management, monitoring, and control. The architecture follows a modular, engine-based design with a robust kernel at its core.

## Core Architecture

### 1. **The Kernel** (kernel.py)
- Central orchestration engine that manages all system operations
- Handles engine initialization and lifecycle management
- Routes commands to appropriate modules
- Manages inter-engine communication
- Provides core utilities: path management, module discovery, sys.path updates

### 2. **The 11 Core Engines**

Ghost Shell uses 11 specialized engines, each with a specific responsibility:

#### 👻 **The GhostCoreEngine** (The Kernel)
- Core system initialization and bootstrapping
- System state management
- Recovery and restart mechanisms

#### 🛡️ **The SecurityEngine** (The Gatekeeper)
- Access control and authentication
- Vault encryption and decryption
- Permission management
- Session security validation

#### 💗 **The HeartbeatEngine** (The Pulse)
- System health monitoring
- Alive signal broadcasting
- Watchdog functionality
- Status polling and reporting

#### ⏰ **The TimeEngine** (The Scheduler)
- Event scheduling and timing
- Reminders and notifications
- Cron-like task execution
- Temporal event management

#### 🌐 **The WebServer** (The Bridge)
- HTTP server for remote access
- REST API endpoint management
- Route handling and request processing
- Web-based command execution

#### 📡 **The HostEngine** (The Dispatcher)
- Inter-process communication
- Network socket management
- Remote command execution
- Host bridging capabilities

#### 🗂️ **The LoaderEngine** (The Librarian)
- Dynamic module loading
- Plugin architecture support
- Code hot-reloading
- Dependency management

#### 📊 **The InfoEngine** (The Observer)
- System information gathering
- Configuration management
- Diagnostic data collection
- Performance metrics tracking

#### 🔔 **The ReminderEngine** (The Heartbeat)
- Background reminder system
- Event notifications
- Scheduled alerts
- User notifications and callbacks

#### 🏦 **The VaultEngine** (The Keeper)
- Secure credential storage
- Encryption/decryption operations
- Key management
- Secret rotation

#### ⚙️ **The HostBridge** (The Connector)
- System process management
- Host connectivity layer
- Auto-discovery capabilities
- Network bridging

## System Layers

```
┌─────────────────────────────────────┐
│  Commands Layer (cmd_*.py)          │  User Interface
│  - Shell, Create, Edit, Help, etc.  │
├─────────────────────────────────────┤
│  Main Router (main.py)              │  Command Routing
│  - PREFLIGHT checks                 │
│  - Command dispatch                 │
├─────────────────────────────────────┤
│  Kernel & Engine Layer (src/core)   │  System Core
│  - 11 Specialized Engines           │
│  - Engine management                │
├─────────────────────────────────────┤
│  System Services                    │  Background Tasks
│  - ReminderPulse thread             │
│  - HeartbeatMonitor                 │
│  - WebServer                        │
├─────────────────────────────────────┤
│  Data Layer (data/)                 │  Persistence
│  - Configuration files              │
│  - Vault storage                    │
│  - Logs                             │
└─────────────────────────────────────┘
```

## Boot Sequence

1. **PREFLIGHT Phase** (PREFLIGHT.py)
   - Python 3.8+ version check
   - Core module availability verification
   - Optional module detection
   - Folder structure validation
   - File permissions check
   - System readiness report

2. **Kernel Initialization** (kernel.py)
   - Engine discovery and registration
   - System state setup
   - Configuration loading

3. **Engine Bootstrap** (src/core/*)
   - Each engine initializes in dependency order
   - Security engine locks down access
   - Heartbeat engine starts monitoring
   - Reminder engine starts background thread

4. **Command Routing** (main.py)
   - Command parser reads user input
   - Command module dynamically loaded
   - Engine context provided to command
   - Result returned to user

## Command Architecture

Each command file (cmd_*.py) implements a standard interface:

```python
def run(args=None):
    """Execute the command with optional arguments"""
    # Implementation here
    pass
```

Commands can:
- Access any engine via kernel.get_engine()
- Spawn background tasks via RemindePulse
- Store/retrieve data via VaultEngine
- Execute system commands via HostEngine
- Check system status via InfoEngine

## Background Services

### ReminderPulse Thread
- Runs as daemon thread in cmd_shell.py
- Monitors reminder queue continuously
- Executes scheduled callbacks
- Handles event notifications
- Non-blocking with configurable check interval

### HeartbeatMonitor
- Runs alongside ReminderPulse
- Polls system health every N seconds
- Reports via InfoEngine
- Triggers alarms on anomalies

## Data Storage

```
data/
├── config/
│   ├── reminder_config.json     # ReminderEngine settings
│   ├── system_config.json       # Global configuration
│   └── vault_config.json        # Vault settings
├── vault/
│   └── secrets.encrypted        # Encrypted credentials
├── logs/
│   ├── system.log
│   ├── commands.log
│   └── errors.log
└── version.json                 # Version tracking
```

## Security Model

- **Multi-layer authentication**: User credentials validated on shell entry
- **Encrypted vault**: All secrets stored with AES encryption
- **Permission matrix**: Role-based command access control
- **Session tokens**: Time-limited access credentials
- **Audit logging**: All command execution logged

## Extensibility

### Adding New Commands
1. Create cmd_newcommand.py in src/commands/
2. Implement run(args=None) function
3. Command auto-discovered by main.py
4. Access engines via kernel.get_engine()

### Adding New Engines
1. Create engine_*.py in src/core/
2. Inherit from base Engine class
3. Register with kernel in kernel.py
4. Commands can access via get_engine()

## Performance Characteristics

- **Startup time**: ~500ms-1s (PREFLIGHT + kernel init)
- **Command execution**: 50-200ms typical
- **Memory footprint**: ~50-80MB baseline
- **ReminderPulse overhead**: <1% CPU when idle

## Dependencies

Core dependencies documented in requirements.txt:
- hashlib: Cryptography
- json: Configuration
- threading: Background tasks
- socket: Networking
- sys, os, platform: System utilities
- pathlib: Path handling
- subprocess: Process execution

## Future Architecture Considerations

- Distributed mode: Multi-host coordination
- Event streaming: Real-time event pipeline
- Plugin marketplace: Third-party engine registry
- GraphQL API: Alternative query interface
- Container support: Docker/Kubernetes integration
