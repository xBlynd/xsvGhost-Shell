# 👻 GHOST SHELL PHOENIX v7.0

**One Stick, Any Computer, Surgical Precision**

A portable Python-based "Life Operating System" - your personal diagnostic weapon, secure journal, system repair kit, and command center that lives on a USB stick.

---

## 🚀 QUICK START

```bash
# Clone or copy to USB stick
git clone <your-repo> /path/to/usb/ghost-shell

# Boot Ghost Shell
cd ghost-shell
python3 src/main.py
```

**First Boot:** You'll be prompted to create a god key. Press Enter to auto-generate.

---

## ✨ WHAT'S WORKING NOW

### 🟢 **FULLY OPERATIONAL**

**All 11 Engines Loaded:**
- ✅ **Ghost Core** - OS detection, portable paths (The Anchor)
- ✅ **Security** - Silent god key authentication, RBAC
- ✅ **Heartbeat** - System health monitoring
- ✅ **Loader** - Dynamic command discovery + hot reload
- ✅ **Root** - Silent system command execution
- ✅ **Pulse** - Background daemon thread scheduler
- ✅ **Vault** - Journal + Todo management
- ✅ **Interface** - Role-based banners and themes
- ✅ **BlackBox** - Network ping with jitter analysis
- ✅ **Ghost** - Cleanup on exit, stealth mode
- ✅ **Sync** - USB detection

**7 Working Commands:**
- `status` - System health and engine status
- `help` - List available commands
- `j add <entry>` - Add journal entry
- `j list` - List recent journals
- `todo add <task>` - Add todo
- `todo list` - List todos
- `ping <host>` - Smart ping with jitter analysis
- `reload <cmd>` - Hot reload commands

---

## 💡 USAGE EXAMPLES

### **Journal Your Day**
```bash
ghost> j add Started rebuilding Ghost Shell with Claude
Added to 2026-02-12.md

ghost> j add Fixed the node_type bug in 10 minutes
Added to 2026-02-12.md

ghost> j list
=== RECENT JOURNALS ===
  2026-02-12 (245 bytes)
```

### **Manage Tasks**
```bash
ghost> todo add Build Legion Mode
Added todo #1

ghost> todo add Integrate Cortex AI
Added todo #2

ghost> todo list
=== ACTIVE TODOS ===
  ○ #1: Build Legion Mode
  ○ #2: Integrate Cortex AI
```

### **Diagnose Network Issues**
```bash
ghost> ping 8.8.8.8

Pinging 8.8.8.8 with 10 packets...

=== PING RESULTS ===
Host: 8.8.8.8
Packets: 10 sent, 10 received (0.0% loss)

Latency:
  Min: 12.3 ms
  Avg: 15.7 ms
  Max: 23.1 ms

Jitter: 3.2 ms (EXCELLENT)

✓ Excellent stability - ideal for real-time applications
```

### **Hot Reload Development**
```bash
# Edit a command file
ghost> reload ping
Reloaded ping

# Changes are live - no restart needed!
```

---

## 🏗️ ARCHITECTURE

### **The 11-Engine Grid**

Each engine is **isolated** - failures are contained, not cascading.

```
┌─────────────────────────────────────────┐
│          GHOST KERNEL                   │
│  (Orchestrator & Message Bus)           │
└─────────────────────────────────────────┘
          │
          ├── Ghost Core (The Anchor)
          ├── Security (The Gatekeeper)
          ├── Heartbeat (Health Monitor)
          ├── Loader (Command Discovery)
          ├── Root (System Execution)
          ├── Pulse (Background Tasks)
          ├── Vault (Data Storage)
          ├── Interface (Visual Output)
          ├── BlackBox (Network Ops)
          ├── Ghost (Stealth & Cleanup)
          └── Sync (USB & File Sync)
```

### **Key Design Patterns**

**The Anchor Pattern** - Portable paths:
```python
ROOT_DIR = Path(__file__).parent.parent.parent.absolute()
# Works from ANY location - USB, cloud, local
```

**Daemon Threads** - Non-blocking background:
```python
threading.Thread(target=work, daemon=True).start()
# Never blocks shell input - perfect for gaming
```

**Silent Execution** - No popup windows:
```python
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
# Stealth on Windows
```

**Hot Reload** - Live development:
```python
importlib.reload(module)
# Edit code, test immediately
```

---

## 📂 PROJECT STRUCTURE

```
ghost-shell-phoenix/
├── src/
│   ├── main.py                 # Entry point
│   ├── core/
│   │   ├── kernel.py           # Orchestrator
│   │   ├── ghost_core.py       # The Anchor
│   │   ├── security_engine.py  # Auth & RBAC
│   │   ├── vault_engine.py     # Journal + Todos
│   │   ├── blackbox_engine.py  # Network ops
│   │   └── ... (all 11 engines)
│   └── commands/
│       ├── cmd_status.py       # System status
│       ├── cmd_j.py            # Journal
│       ├── cmd_todo.py         # Task mgmt
│       ├── cmd_ping.py         # Smart ping
│       └── ... (drop-in commands)
├── data/
│   ├── keys/                   # god.key, guest.key
│   ├── vault/
│   │   ├── journal/            # Markdown journals
│   │   └── todos/              # JSON todos
│   └── session/                # State files
└── README.md
```

---

## 🎯 ROADMAP

### **Phase 1: Foundation** ✅ COMPLETE
- All 11 engines operational
- Core commands working
- USB portability confirmed
- Hot reload functional

### **Phase 2: Distributed (Next)**
- Legion Mode - Multi-device coordination
- Master/Legionnaire architecture
- Remote command execution
- Fleet monitoring

### **Phase 3: AI Integration**
- Cortex Engine - Local Ollama integration
- Natural language commands
- AI-assisted diagnostics
- Code generation

### **Phase 4: Advanced**
- Wraith Installer - One-click deployment
- Advanced network scanning
- Encrypted vault storage
- Cross-platform sync

---

## 🔒 SECURITY

**God Key Authentication:**
- First boot creates god.key from passphrase
- Silent auth on subsequent boots (if key exists)
- No prompts = no evidence

**Role Hierarchy:**
- **GOD** - Full access (dangerous commands)
- **ADMIN** - Standard diagnostics
- **GUEST** - Read-only tools

**Stealth Features:**
- Cleanup on exit (removes .pyc, __pycache__)
- Silent subprocess execution
- Minimal process footprint

---

## 💻 REQUIREMENTS

- **Python:** 3.8+ (for portability)
- **Dependencies:** stdlib only for core
- **Optional:** `psutil` for enhanced health monitoring

**No installation required** - runs directly from USB.

---

## 🎨 CUSTOMIZATION

### **Adding Commands**

Drop a file in `src/commands/cmd_yourname.py`:

```python
"""Your Command - Description"""

HELP = "Usage: yourname <args>"

def execute(kernel, args):
    # Your logic here
    return "Output to user"
```

Restart or `reload all` - command is live!

### **Engine Access**

```python
def execute(kernel, args):
    # Get engines
    vault = kernel.engines.get('vault')
    security = kernel.engines.get('security')
    
    # Use them
    if security.has_permission(Role.GOD):
        vault.journal_add("Did dangerous thing")
```

---

## 🐛 TROUBLESHOOTING

**Shell won't boot:**
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Check for errors
python3 src/main.py
```

**God key issues:**
```bash
# Delete and regenerate
rm data/keys/god.key
python3 src/main.py
```

**Command not found:**
```bash
ghost> reload all
Reloaded all commands
```

---

## 📜 LICENSE

MIT License - Build whatever you want.

---

## 🙏 ACKNOWLEDGMENTS

Built with:
- Python standard library
- Bloodyminded determination
- Claude Code (AI pair programmer)
- The belief that your OS should work for YOU

---

**"One Stick, Any Computer, Surgical Precision"**

This is YOUR Life OS. Make it yours.

EOF
