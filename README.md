<!-- THIS DOCUMENT MAY BE OLD. THIS COMMENT MADE 2026-02-11 2:09AM EST. -->

# 🌌 xsvCommandCenter: The Digital Life Container

**Version:** **v6.0-Ghost** (Build 3)
**Status:** Alpha / Active Development
**Philosophy:** "One Stick, Any Computer, Surgical Precision."

---

## 🎯 The Grand Vision
This is not just a script. It is a **Portable Operating Environment**.
It is designed to be the single repository for my entire digital life—my brain, my tools, my games, and my work—capable of running on **any** machine (Windows, Linux, ParrotOS, MacOS) instantly without installation.

### The "Split-Brain" Architecture
1.  **The Brain (GitHub):** The Logic, Engines, and Public Scripts. (Syncs everywhere).
2.  **The Soul (USB/Cloud):** My Journals, Passwords, Device States, and Private Configs. (Never touches public Git).

---

## 🏗️ System Architecture

### 1. The Core (`src/core/`)
The "Organs" of the system. Commands utilize these engines to do heavy lifting.
* **`InfoEngine`**: The Detective. Identifies Host OS, Hardware, and verifies Integrity.
* **`HostEngine`**: The Worker. Handles file ops, process killing, and launching.
* **`ReminderEngine`**: The Pulse. Handles Scheduling, Relative Time (`10m`, `1h`), and Toast Notifications.
* **`VaultAPI`**: The Memory. Manages JSON-based storage (Todo, Journals).

### 2. The Ghost Shell (`src/commands/cmd_shell.py`)
A persistent, conscious terminal (`xsv@HOST >`).
* **The Heartbeat**: A background thread (`ReminderPulse`) that watches time while you work.
* **Hot Reload**: Updates code in memory (`reload`) without restarting the shell.
* **Self-Healing**: Automatically repairs missing folders and purges cache (`repair`).

---

## 🔮 The Module Roadmap

### 🛠️ The "Ghost" Utilities (LIVE)
* **Task Master (`todo`)**:
    * Natural Language: `todo add "Call Mom" --due 10m` (Auto-calculates time).
    * Smart Lists: Work, Home, and xsv project tracking.
* **Quick Reminders (`remind`)**:
    * Fire-and-forget timers: `remind "Pizza" 15m`.
    * **Cross-Platform Toasts**: Native Windows Notifications or Linux `notify-send`.
* **Diagnostics (`status`)**:
    * Real-time integrity stream checks every module for syntax errors.
* **The Repairman (`repair`)**:
    * One-click system restoration (Folder structure, Configs, Cache purge).

### 🛠️ Development (`cmd_dev.py`)
* **Granular Installation**:
    * `dev install vscode`: Installs VS Code + My Extensions (checks OS first).
* **Environment Sync**:
    * `dev sync`: Pulls my latest VS Code settings/keybindings from Vault.

### 🌐 Web Server (`cmd_web.py`)
* **Smart Launch**: `web serve`: Instantly hosts current folder on LAN.

---

## 📂 Data Strategy

| Zone | Content | Storage Location |
| :--- | :--- | :--- |
| **SYSTEM** | Core Logic, Router, Base Modules | `src/commands/` |
| **USER** | Custom Scripts, Pranks, Tools | `src/commands/custom/` |
| **LIBRARY** | 3rd Party Scripts (Bash/PS1) | `library/` (Linked via JSON) |
| **VAULT** | Private Todos, Journals, Configs | `data/vault/` (GitIgnored) |

---

## 🚀 Usage Guide
1.  **Plug in USB.**
2.  **Double-click `LAUNCH.bat`.**
3.  **Login** (Secure Shell opens).
4.  **Command:** `status` (Check system health).
5.  **Command:** `todo list` (See what's next).

---

## 📚 Complete Documentation

Ghost Shell has comprehensive documentation for developers, users, and operators:

### Core Documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design, all 11 engines, and boot sequence
- **[COMMANDS.md](COMMANDS.md)** - Complete command reference for 25+ commands
- **[API_REFERENCE.md](API_REFERENCE.md)** - REST API endpoints, WebSocket events, and client libraries
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues, solutions, and performance tuning

### Getting Started
- **[INSTALLATION.md](INSTALLATION.md)** - Installation guide and prerequisites
- **[SECURITY.md](SECURITY.md)** - Vault encryption and security best practices

### Development
- **[ENGINE_MANIFEST.md](ENGINE_MANIFEST.md)** - Details on all 11 core engines
- **[THREAD_HANDOFF.md](THREAD_HANDOFF.md)** - Session summary for multi-thread development

### Quick Links
- Ghost System Atlas (Design): `docs/Ghost Shell Design Phase/🗺️ The Ghost System Atlas_master-draft.md`
- GitHub Repository: https://github.com/xBlynd/xsvGhost-Shell
- Issues & Feature Requests: https://github.com/xBlynd/xsvGhost-Shell/issues

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Review [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system
2. Check [COMMANDS.md](COMMANDS.md) for command structure
3. Create a new branch for your feature
4. Follow the existing code style
5. Submit a pull request with documentation

## 📄 License

Ghost Shell is licensed under the MIT License. See LICENSE file for details.

---

**Built with ❤️ by xBlynd**
**Philosophy: "One Stick, Any Computer, Surgical Precision."**
