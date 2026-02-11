# Ghost Shell OS - System Structure, Data Architecture & Sync System

## 📁 Complete Folder Structure

```
xsvGhost-Shell/
├── README.md (root entry point)
├── LAUNCH.bat (Windows startup)
├── PREFLIGHT.py (system verification)
├── pack_context.py (context packaging)
│
├── src/ (CORE ENGINE & EXECUTION)
│   ├── core/ (THE 11 ENGINES)
│   │   ├── engine_ghostcore.py (👻 GhostCoreEngine - Brain & Environment)
│   │   ├── engine_shield.py (🛡️ ShieldEngine - Defense & Authentication)
│   │   ├── engine_ghost.py (👻 GhostEngine - Offensive Stealth & Anti-Forensics)
│   │   ├── engine_blackbox.py (📡 BlackBoxEngine - Network Dominance)
│   │   ├── engine_root.py (⚡ RootEngine - Host Control / God Mode)
│   │   ├── engine_pulse.py (⏳ PulseEngine - Scheduling & Consciousness)
│   │   ├── engine_vault.py (📚 VaultEngine - Data Management)
│   │   ├── engine_sync.py (🔄 SyncEngine - Data Transport)
│   │   ├── engine_interface.py (📺 InterfaceEngine - UI & Face)
│   │   ├── engine_loader.py (🧩 LoaderEngine - Expansion & Routing)
│   │   └── engine_heartbeat.py (💓 HeartbeatEngine - Immune System)
│   │
│   ├── commands/ (COMMAND MODULES)
│   │   ├── cmd_shell.py (main shell loop - runs ReminderPulse & HeartbeatMonitor)
│   │   ├── cmd_help.py
│   │   ├── cmd_status.py
│   │   ├── cmd_vault.py (vault management)
│   │   ├── cmd_sync.py (manual sync control)
│   │   └── ...(other commands)
│   │
│   ├── kernel.py (ORCHESTRATOR - manages all engines)
│   └── main.py (COMMAND ROUTER - entry point)
│
├── library/ (EXTERNAL SCRIPTS & TOOLS)
│   ├── matrix_prank.py
│   └── ...(utility scripts, loaded dynamically)
│
├── data/ (PERSISTENT DATA & CONFIGURATION)
│   ├── config/
│   │   ├── settings.json (global settings, synced to Vault)
│   │   ├── reminder_config.json (PulseEngine scheduling)
│   │   ├── vault_config.json (VaultEngine encryption settings)
│   │   └── sync_config.json (SyncEngine rules & USB exclusions)
│   │
│   ├── vault/ (ENCRYPTED PERSONAL FILES - SYNCED)
│   │   ├── notes/ (Markdown notes)
│   │   ├── journals/ (Daily journals, encrypted)
│   │   ├── todos/ (Task list & reminders)
│   │   ├── secrets.encrypted (credentials, API keys - Fernet encrypted)
│   │   ├── loot/ (data gathered from operations)
│   │   └── library/ (personal knowledge base)
│   │
│   ├── logs/ (AUDIT TRAIL - SYNCED)
│   │   ├── system.log (kernel & engine events)
│   │   ├── commands.log (all command execution)
│   │   ├── errors.log (crash reports)
│   │   └── sync.log (sync operations)
│   │
│   └── metadata/
│       ├── .lastSync (timestamp of last manual/remote sync)
│       ├── .syncIgnore (patterns to exclude from USB sync)
│       └── version.json (current system version)
│
├── docs/ (DOCUMENTATION - STATIC)
│   ├── README.md (documentation entry)
│   ├── guides/ (LIVING DOCUMENTATION)
│   │   ├── index.md (doc hub - main navigation)
│   │   ├── SYSTEM_STRUCTURE_AND_DATA_FLOW.md (THIS FILE)
│   │   ├── 🗺️ The Ghost System Atlas - Engine Map.md (AUTHORITATIVE engine definitions)
│   │   ├── ARCHITECTURE.md (TO BE UPDATED - sync with Engine Map)
│   │   ├── commands.md (all commands reference)
│   │   ├── getting-started.md (beginner guide)
│   │   ├── SECURITY.md
│   │   ├── TROUBLESHOOTING.md
│   │   └── AI/ (AI session management)
│   │       ├── THREAD_TAKEOVER_MASTER.md (AI session handoff)
│   │       └── SESSION_COMPLETION_REPORT.md
│   │
│   └── Ghost Shell Design Phase/ (ARCHIVED - ORIGINAL VISION)
│       └── 🗺️ The Ghost System Atlas_master-draft.md
│
├── tests/ (TESTING SUITE)
│   ├── test_engines.py
│   ├── test_sync.py
│   └── test_vault.py
│
└── .gitignore
```

---

## 📚 The Document Library/Doc Hub System

### Purpose
The **Doc Hub** (`/docs/guides/index.md`) serves as the central navigation and knowledge management system for Ghost Shell OS. It organizes:

- **System Documentation** - How Ghost Shell works internally
- **User Guides** - How to use Ghost Shell commands
- **Personal Knowledge Base** - Your research, notes, loot
- **Metadata** - Tags, links, cross-references

### Architecture

```
Doc Hub (index.md)
├── System Core (Links to Engine Map, Architecture, etc.)
├── Command Reference (Dynamically generated from cmd_*.py)
├── User Guides (Getting started, security, troubleshooting)
├── Personal Vault (Notes, journals, todos - SYNCED)
│   ├── 📝 Notes (quick capture, linked)
│   ├── 📓 Journals (dated entries, searchable)
│   ├── ✅ Todos (tasks with reminders via PulseEngine)
│   └── 🎯 Loot (research data, findings)
└── Session Records (AI handoff docs, completion reports)
```

### File Organization

**Life Files** (Personal, SYNCED):
```
data/vault/
├── notes/
│   ├── research.md (organized by topic)
│   ├── ideas.md
│   └── quick-capture.md (rapid entry)
├── journals/
│   ├── 2026-02-11.md (daily)
│   └── 2026-01.md (monthly summary)
├── todos/
│   ├── active.md (current tasks)
│   ├── backlog.md (future)
│   └── completed.md (archive)
└── loot/
    ├── osint/ (reconnaissance data)
    ├── exploits/ (findings)
    └── configs/ (captured configs)
```

**Core Files** (System, NOT synced by default):
```
src/
├── core/ (11 engines - immutable)
├── commands/ (command modules - immutable)
└── kernel.py (orchestrator - immutable)
```

---

## 🔄 The Sync System: Bridging Life Files & Core

### The Challenge
You work on Ghost Shell from:
- ✅ USB stick (primary portable environment)
- ✅ Multiple computers/VMs (temporary environments)
- ✅ No device (cloud sync? mobile app? future)

But your **life files** (notes, journals, todos, research) must:
- ✅ Sync BACK to primary location
- ✅ Never lose data
- ✅ Stay encrypted on untrusted machines
- ✅ Separate from system core (don't want to sync entire Ghost Shell)

### Sync Architecture

#### **Mode 1: Manual USB Sync** (Primary - Implemented Now)
```
Workflow:
1. USB Device (xsvGhost-Shell/) plugged into Host Machine
2. User runs: ghost sync --pull
   - Downloads any NEWER vault/ from secondary location (cloud, remote server, phone)
   - Updates local vault/ with latest
3. User works on Ghost Shell, edits notes, runs commands
4. User runs: ghost sync --push
   - Uploads vault/ to secondary location via SyncEngine
   - Marks as synced in .lastSync
5. Unplug USB, move to next machine
6. Repeat: sync --pull → work → sync --push

Configuration: /data/config/sync_config.json
{
  "mode": "manual_usb",
  "vault_path": "data/vault/",
  "exclude": ["src/", "library/"],  // Don't sync core system
  "secondary_location": "usb://encrypted_backup/",
  "encryption": "fernet",  // Always encrypted
  "last_sync": "2026-02-11T03:00:00Z"
}
```

#### **Mode 2: Remote Sync** (Future - Not Yet Implemented)
```
Workflow:
1. Ghost Shell on USB detects internet connection
2. Connects to remote server (self-hosted, encrypted)
3. Automatic background sync:
   - Every 30 minutes (configurable)
   - Only syncs vault/ (life files)
   - Uses encrypted tunnel (SSH/TLS)
4. If device is lost/compromised:
   - Remote backup ensures data recovery
   - Can restore to new USB from any machine

Configuration: /data/config/sync_config.json
{
  "mode": "remote",
  "vault_path": "data/vault/",
  "exclude": ["src/", "library/"],
  "remote_server": "sync.ghostshell.local",
  "remote_path": "/backups/user/ghost/vault/",
  "sync_interval_minutes": 30,
  "encryption": "fernet",
  "auth": "ssh_key"
}
```

### SyncEngine Responsibilities
1. **Detect Mode**: Check config, determine sync method
2. **Encryption/Decryption**: Always encrypt vault/ before transmission
3. **Conflict Resolution**: If both local and remote have changes:
   - Newest timestamp wins (by default)
   - Or prompt user to choose
4. **Logging**: Record all sync operations in data/logs/sync.log
5. **Verification**: Hash check after sync to ensure integrity

### What Syncs vs What Doesn't

| File/Folder | Syncs? | Reason |
|---|---|---|
| `data/vault/notes/` | ✅ YES | Personal knowledge base |
| `data/vault/journals/` | ✅ YES | Life records, encrypted |
| `data/vault/todos/` | ✅ YES | Task management, critical |
| `data/vault/secrets.encrypted` | ✅ YES | Credentials (already encrypted) |
| `data/config/` | ⚠️ PARTIAL | Only sync_config.json, not settings.json |
| `data/logs/` | ❌ NO | Too large, machine-specific |
| `src/` | ❌ NO | Core system (use git for updates) |
| `library/` | ❌ NO | Scripts (use git for updates) |
| `docs/` | ❌ NO | Static docs (use git) |

---

## 📝 Personal Data Management

### Notes System
**Stored**: `data/vault/notes/`
**Format**: Markdown
**Features**:
- Tags: `#research #osint #exploit`
- Links: Cross-reference between notes
- Search: VaultEngine searches all notes for keywords
- Encrypted at rest: Fernet encryption

### Journal System  
**Stored**: `data/vault/journals/`
**Format**: Dated markdown files (YYYY-MM-DD.md)
**Features**:
- Auto-timestamp entries
- Monthly summaries (2026-02.md)
- Searchable by date
- Private & encrypted

### Todo/Reminder System
**Stored**: `data/vault/todos/`
**Managed by**: PulseEngine (scheduler)
**Features**:
- Active.md (current tasks with priorities)
- Backlog.md (future work)
- Completed.md (archive with dates)
- PulseEngine triggers notifications based on schedule
- Integrates with ReminderPulse background thread

### Loot Management
**Stored**: `data/vault/loot/`
**Format**: Organized by category
**Content**:
- OSINT findings
- Captured configurations
- Exploit data
- Research artifacts

---

## 🔗 Data Flow Example: Adding a Note

```
1. User runs: ghost note "Found new SSH key"
2. InterfaceEngine captures input
3. VaultEngine creates: data/vault/notes/quick-capture.md entry
4. Encrypts entry with ShieldEngine (Fernet key)
5. Logs action in data/logs/commands.log
6. PulseEngine checks if reminder needed
7. On sync --push:
   - SyncEngine reads encrypted vault/
   - Uploads to secondary location
   - Records timestamp in .lastSync
8. On new machine sync --pull:
   - SyncEngine downloads vault/
   - Decrypts with ShieldEngine
   - User can access note
```

---

## 🎯 Next Steps
1. Implement RemoteSync mode (RootEngine + SyncEngine)
2. Add mobile app for Todo/Note access without USB
3. Create cloud sync option (encrypted, self-hosted)
4. Build conflict resolution UI for competing edits
5. Add backup scheduling & verification
