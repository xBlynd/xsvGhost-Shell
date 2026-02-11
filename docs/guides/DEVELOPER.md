# (The Manual)
Changes: Added the "Engine Pattern" (Logic vs Command). Added instructions for the Repair Protocol. Explained how to add features safely.

Markdown

# 🛠️ xsvCommandCenter Developer Guide

**Target Audience:** Hackers, Developers, and Future Ian.
**Goal:** Expand the system without breaking the Core.

---

## 👻 1. The Ghost Shell Architecture
The Ghost Shell (`src/commands/cmd_shell.py`) is an **Infinite Loop** that acts as a traffic controller. It does not "know" commands; it routes them.

### The Routing Logic (Order of Operations)
1.  **Hardcoded Aliases:** Checks `cmd_shell.py` (exit, clear, reload).
2.  **System Modules:** Checks `src/commands/cmd_*.py`.
3.  **Custom Modules:** Checks `src/commands/custom/cmd_*.py`.
4.  **Magic Commands (JSON):** Checks `data/config/commands.json` (Links to `library/`).
5.  **System Fallback:** Passes to Host OS (cmd/bash).

---

## 🧩 2. The "Engine" Pattern
We separate **Logic** from **Interface**.
* **The Command (`src/commands/`)**: Parses user arguments (argparse), prints to screen.
* **The Engine (`src/core/`)**: Does the math, saves files, talks to OS.

**Example:**
* `cmd_todo.py`: Accepts `--due 10m`.
* `reminder_engine.py`: Calculates that `10m` = `18:45:00`.

### Why?
So other tools can use the logic. The `shell` uses the `ReminderEngine` to check background alerts without running the `todo` command.

---

## ⚡ 3. How to Add Features

### Method A: The Wizard (Recommended)
1.  **Type:** `create command mytool`
2.  **Enter Description:** "My cool tool"
3.  **Result:** Auto-generates `src/commands/custom/cmd_mytool.py`.

### Method B: The Library Link (Scripts)
**Best for:** Running a PowerShell/Bash script you found online.
1.  Drop script into `library/` (e.g., `library/matrix.py`).
2.  Open `data/config/commands.json`.
3.  Add it:
    ```json
    "matrix": { "type": "script", "path": "library/matrix.py" }
    ```

---

## ⚠️ Critical Rules

### 1. Threading is Mandatory for GUI
If your command opens a window (Tkinter, PyGame), use a thread or you will freeze the shell.
```python
t = threading.Thread(target=my_gui_func, daemon=True)
t.start()
2. The Repair Protocol
If things act weird (old code running, imports failing):

Run repair (Purges __pycache__).

Run reload (Restarts the Heartbeat).

3. File Paths
Never hardcode C:\. Always use relative paths:

Python

ROOT = Path(__file__).parent.parent.parent

---

### 3. `TODO.md` (The Worklist)
* **Changes:** Checked off Phase 1 & 2 items (Repair, Status, Relative Time). Added new Phase 3 items based on our chat (Journal Viewer, Visual Polish).

```markdown
# 📋 Project Worklist

## 🔥 Phase 1: The Foundation (COMPLETED)
- [x] **Modular Architecture:** Core vs. Commands.
- [x] **Dynamic Router:** Auto-loads modules from `src/commands`.
- [x] **Ghost Shell:** Interactive terminal with Sticky Headers.
- [x] **Launchers:** `LAUNCH.bat` (Windows).
- [x] **Self-Healing:** `cmd_repair.py` (Cache wipe & Folder fix).

## 🛠️ Phase 2: The Conscious OS (COMPLETED)
- [x] **The Heartbeat:** Background thread (`ReminderPulse`) for alerts.
- [x] **Time Engine:** Relative time parsing (`10m`, `1h`, `30s`).
- [x] **Notifications:** Cross-platform Toasts (Windows PowerShell / Linux `notify-send`).
- [x] **Diagnostics:** `cmd_status.py` with real-time integrity streaming.
- [x] **Hot Reload:** True module reloading in memory.

## 🚧 Phase 3: The Toolbelt (Active Development)
- [ ] **Journal Viewer:** Read `.md` logs directly in terminal (Pagination/Search).
- [ ] **Visual Polish:** Color-coded categories (Work=Blue, Home=Green).
- [ ] **`cmd_dev.py`**:
    - [ ] `install vscode` (Auto-detect OS).
    - [ ] `sync settings` (Pull extensions list).
- [ ] **`cmd_web.py`**:
    - [ ] `serve`: Simple HTTP server wrapper.
- [ ] **`cmd_clean.py`**:
    - [ ] Temp file wiper / Browser cache cleaner.

## 🔭 Phase 4: Expansion (Advanced)
- [ ] **`cmd_gameserver.py`**: Minecraft/Ark installers.
- [ ] **`cmd_ai.py`**: Gemini API hook.
- [ ] **ParrotOS Verification**: Test all `notify-send` and path logic on Linux.
- [ ] **Network Monitor**: Live latency tracker for gaming troubleshooting.

## 📜 Pivot Log
* *Pivoted `DependencyEngine` into `cmd_dev.py`.*
* *Split `ReminderEngine` to handle both Todo Lists and Quick Timers.*
* *Moved `desktop.ini` handling to `repair` script and `.gitignore`.*
