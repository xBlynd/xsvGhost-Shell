# 📇 ENGINE MANIFEST - The 11 Engines of Ghost Shell

## Complete Engine Registry

This document serves as the single source of truth for all 11 engines powering xsvGhost-Shell v6.0.

---

## 1. 👻 The GhostCoreEngine (The Kernel)

**Status:** ✅ IMPLEMENTED  
**File:** `src/core/ghost_core_engine.py`  
**Loaded By:** `kernel.py` (first)  

**Role:** The Brain & Environment Detector

**Responsibilities:**
- OS Detection (Windows/Linux/macOS)
- Config loading from `data/config/settings.json`
- Dependency checking (Python, Node, libnotify)
- Initial environment setup
- IS_LINUX flag for other engines

**Key Methods:**
```python
detect_os()          # Returns OS type
load_config()        # Reads settings.json
check_dependencies() # Verifies required tools
```

---

## 2. 🛡️ The SecurityEngine (The Gatekeeper)

**Status:** ✅ IMPLEMENTED  
**File:** `src/core/security_engine.py`  
**Loaded By:** `kernel.py` (second)  

**Role:** Defense & Authentication

**Responsibilities:**
- PBKDF2 master key derivation from password
- Fernet encryption/decryption of vault files
- Login system & password validation
- 5-minute session timeout
- Master key management (RAM only)

**Key Methods:**
```python
authenticate(password)     # Verify user
derive_key(password)       # Generate master key
encrypt(data, key)         # Encrypt vault content
decrypt(data, key)         # Decrypt vault content
auto_lock()               # 5-min timeout handler
```

---

## 3. 👻 The GhostEngine (The Phantom)

**Status:** ⚠️ PARTIAL (v6.0)  
**File:** `src/core/ghost_core_engine.py` (needs refactor)  
**Loaded By:** `kernel.py` (on-demand)  

**Role:** Offensive Stealth & Anti-Forensics

**Responsibilities:**
- Active stealth / "Ghost Mode" (PID hiding)
- Timestamp wiping on file operations
- Clipboard scrubbing on exit
- Anti-forensic trace wiper
- Memory wiping of sensitive data
- PowerShell reflection for payload delivery (Windows)

**Key Methods:**
```python
enable_ghost_mode()   # Hide process
wipe_timestamps()     # Reset file times
clear_clipboard()     # Windows/Linux compatible
wipe_memory()        # Overwrite sensitive RAM
```

**Future Implementation:**
- PID spoofing for advanced stealth
- ShellBags cleanup (Windows)
- Event log wiping capabilities

---

## 4. 📡 The BlackBoxEngine (The Shadow Network)

**Status:** 🚧 PLANNED (v7.0)  
**File:** `src/core/blackbox_engine.py` (placeholder)  

**Role:** Network Dominance & Forensics

**Responsibilities:**
- Headless incognito browser (curl/requests with spoofed UA)
- Traffic interception & analysis
- Promiscuous mode scanning
- SSH tunneling & reverse shells
- Packet loss variance logging for ISP troubleshooting
- Network anomaly detection

**Key Methods:**
```python
incognito_search()       # Spoofed Google/Perplexity searches
capture_traffic()       # Network sniffing
scan_subnet()          # Discover local devices
create_tunnel()        # SSH reverse tunnels
analyze_latency()      # Logging jitter/lag
```

---

## 5. ⚡ The RootEngine (The Mechanic)

**Status:** ✅ IMPLEMENTED (partial)  
**File:** `src/core/host_engine.py` (refactor needed - rename to root_engine.py)  
**Loaded By:** `kernel.py`  

**Role:** Host Control / God Mode

**Responsibilities:**
- System registry hacks (Windows)
- Process termination (force kill)
- Hardware ID spoofing/reading (HWID, MAC)
- User account management
- System tuning & debloating
- TCP/IP optimization

**Key Methods:**
```python
kill_process(pid)       # Force terminate
read_hwid()            # Get hardware serial
spoof_hwid()           # Change HWID
tune_tcp()             # Optimize network
disable_telemetry()    # Windows debloat
```

---

## 6. ⏳ The PulseEngine (The Timekeeper)

**Status:** ✅ IMPLEMENTED  
**File:** `src/core/reminder_engine.py` (RENAME TO pulse_engine.py)  
**Loaded By:** `kernel.py`  

**Role:** Scheduling & Consciousness

**Responsibilities:**
- Cron-style task scheduling
- Relative time parsing ("10m", "1h", "next friday")
- Toast notifications (Windows/Linux)
- Background task execution
- Heartbeat pulse (system alive check)

**Key Methods:**
```python
schedule_task(cmd, time)    # Cron scheduling
parse_relative_time(str)    # "10m" -> timestamp
show_toast(title, msg)      # Native notifications
get_pulse()                # System heartbeat
```

---

## 7. 📚 The VaultEngine (The Librarian)

**Status:** ✅ IMPLEMENTED  
**File:** `src/core/vault_api.py`  
**Loaded By:** `kernel.py`  

**Role:** Data Management

**Responsibilities:**
- CRUD operations on vault files
- JSON/Markdown file handling
- Search indexing across vault
- Folder structure repair
- Encryption hook to SecurityEngine
- Backup/restore operations

**Key Methods:**
```python
read_vault(filename)        # Load encrypted file
write_vault(filename, data) # Save encrypted
search(keyword)            # Find in vault
repair_structure()         # Fix missing folders
backup()                   # Create timestamped backup
restore(backup_file)       # Restore from backup
```

---

## 8. 🔄 The SyncEngine (The Bridge)

**Status:** 🚧 PLANNED (v7.0)  
**File:** `src/core/sync_engine.py` (placeholder)  

**Role:** Data Transport

**Responsibilities:**
- One-way sync (Vault ↔ Host)
- Silent file transfer (no timestamp updates)
- Conflict resolution
- Cloud sync to OneDrive/Google Drive/Dropbox
- Version control for vault changes

**Key Methods:**
```python
sync_to_host()          # Vault -> Host
sync_from_host()        # Host -> Vault
silent_copy()          # cp without timestamps
resolve_conflicts()    # Merge strategy
sync_to_cloud()        # Cloud backup
```

---

## 9. 📺 The InterfaceEngine (The Face)

**Status:** ✅ IMPLEMENTED (partial)  
**File:** `src/commands/cmd_shell.py` + `src/core/interface_engine.py`  

**Role:** UI, Help, and Alias Manager

**Responsibilities:**
- Dynamic help menu generation
- Alias management (shortcuts)
- Terminal theming (Blue/Red/Custom)
- Spinner/loader animations
- Prompt customization
- Command autocomplete

**Key Methods:**
```python
generate_help()        # Build help menu
set_alias(short, cmd) # Create command shortcuts
set_theme(color)       # Change UI theme
show_spinner()        # Loading animations
generate_prompt()     # Custom shell prompt
```

---

## 10. 🧩 The LoaderEngine (The Nervous System)

**Status:** ✅ IMPLEMENTED  
**File:** `src/core/loader_engine.py`  
**Loaded By:** `kernel.py`  

**Role:** Expansion & Routing

**Responsibilities:**
- Hot-swap command detection
- Manifest parsing (metadata)
- Dependency checking before execution
- Auto-loading from `src/commands/custom/`
- Library script linking
- Dynamic command registration

**Key Methods:**
```python
load_command(name)           # Load cmd_*.py
parse_manifest(file)         # Read metadata
check_dependencies(cmd)      # Verify tools
auto_discover_commands()    # Scan for new cmds
link_library_scripts()       # External script support
```

---

## 11. 💓 The HeartbeatEngine (The Immune System)

**Status:** ✅ IMPLEMENTED (partial)  
**File:** `src/core/heartbeat_engine.py`  
**Loaded By:** `kernel.py` (continuous)  

**Role:** Vital Signs & Diagnostics

**Responsibilities:**
- Self-healing (restore corrupted files)
- Integrity pulse (hash verification)
- Crash handler & error logging
- Engine status monitoring
- Vault health checks
- Ghost mode status tracking
- Performance metrics collection

**Key Methods:**
```python
check_integrity()      # File hash verification
self_heal()           # Restore from backup
log_crash(error)      # Error logging
get_engine_status()   # Monitor all engines
monitor_vault()       # Vault health
get_metrics()         # Performance data
```

---

## Engine Initialization Order

**Boot Sequence:**

```python
1. GhostCoreEngine    # Detect OS, load config
2. SecurityEngine     # Password auth, key generation
3. HeartbeatEngine    # Integrity check
4. VaultEngine        # Load vault structure
5. PulseEngine        # Start scheduler
6. LoaderEngine       # Discover commands
7. RootEngine         # System capabilities
8. InterfaceEngine    # Initialize UI
9. GhostEngine        # Optional stealth mode
10. BlackBoxEngine    # Optional (v7.0)
11. SyncEngine        # Optional (v7.0)
```

**Total Boot Time:** ~500ms (target)

---

## Engine Status Command

```bash
xsv> status

👻 GhostCoreEngine: ✅ OK (Windows 11, Python 3.11)
🛡️ SecurityEngine: ✅ OK (Password set, 2FA disabled)
👻 GhostEngine: ✅ READY (Ghost mode: OFF)
📡 BlackBoxEngine: ⏳ NOT LOADED
⚡ RootEngine: ✅ OK (Admin rights available)
⏳ PulseEngine: ✅ OK (5 tasks scheduled)
📚 VaultEngine: ✅ OK (12 files, 2.3MB, all encrypted)
🔄 SyncEngine: ⏳ NOT LOADED
📺 InterfaceEngine: ✅ OK (Theme: blue)
🧩 LoaderEngine: ✅ OK (18 custom commands)
💓 HeartbeatEngine: ✅ OK (Last check: 2 min ago)

✅ System Health: 100% - All critical engines nominal
```

---

## Planned Enhancements

**v6.5:**
- GhostEngine: PID spoofing + ShellBags cleanup
- PulseEngine: Advanced time parsing
- HeartbeatEngine: Real-time performance monitoring

**v7.0:**
- BlackBoxEngine: Full implementation
- SyncEngine: Cloud backup + conflict resolution
- SecurityEngine: Hardware keyfile + 2FA

**v8.0:**
- Hardware security module support
- Distributed engine architecture
- Remote engine execution

---

**Last Updated:** February 11, 2026  
**Version:** Manifest v1.0 (Ghost Shell v6.0)  
**Status:** Complete engine registry established
