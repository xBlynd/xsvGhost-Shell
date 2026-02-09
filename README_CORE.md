# ⚙️ xsvCommandCenter: The Core Mechanics

**Warning:** This document describes the internal "Brain" and "Engine" of xsv.
**Do not edit files in `src/core/` unless you are upgrading the OS architecture.**

---

## 🧠 1. The Brain: Dynamic Routing (`src/main.py`)
The Brain is a "Traffic Controller." It does not know what commands exist until it runs.
* **Startup:** It scans `src/commands/` for files starting with `cmd_`.
* **Execution:**
    1.  Receives `xsv [cmd] [args]`.
    2.  Tries to `import src.commands.cmd_[cmd]`.
    3.  If found -> Runs `.run(args)`.
    4.  If not found -> Checks `data/config/commands.json`.
* **Why this matters:** You can drop a file named `cmd_pizza.py` into the folder, and `xsv pizza` works instantly. No registration required.

---

## 🔧 2. The Engine: Hardware Abstraction (`src/core/`)
These scripts are "Pure Python." They never print to the user; they only return data or perform actions.

### A. `info_engine.py` (The Detective)
* **Role:** Read-Only Scanner.
* **Key Function:** `scan_windows_deep()`
    * Uses PowerShell `Get-CimInstance` to mimic CPU-Z.
    * Returns a JSON object with CPU, RAM, GPU, and Cloud Drive paths.
* **Maintenance:** Edit this if you need to detect a new piece of hardware (e.g., a specific drone or 3D printer).

### B. `host_engine.py` (The Worker)
* **Role:** Action Executor.
* **Key Functions:**
    * `nuke(path)`: Force deletes files/folders.
    * `launch(path)`: Opens files in default OS app.
    * `run_sys_command(cmd)`: Wrapper for `subprocess.run` to handle errors safely.
* **Maintenance:** Edit this if you add support for a new OS (e.g., adding MacOS specific launch logic).

---

## 👻 3. The Ghost Shell (`src/commands/cmd_shell.py`)
This is the interactive loop. It sits *on top* of the Core.
* **The Loop:** `while True: input()`.
* **The Three Modes:**
    1.  **Smart:** Tries Internal -> Magic -> System.
    2.  **Exec:** Forces System (`exec ping`).
    3.  **Raw:** Drops to OS Shell (`sh`).
* **Maintenance:** Edit this to change the "Look and Feel" (Colors, Header, Prompt).

---

## 🏗️ 4. Data Storage Strategy
* **Code:** `src/` (Syncs to GitHub).
* **Config:** `data/config/` (Syncs to GitHub).
* **Private:** `data/vault/` (**IGNORED** by Git).
    * *Rule:* Never hardcode API keys in `src/`. Always read from `secrets.json`.