# 🛠️ xsvCommandCenter Developer Guide

**Target Audience:** Hackers, Developers, and Future Ian.
**Goal:** Expand the system without breaking the Core.

---

## 👻 1. The Ghost Shell Architecture
The Ghost Shell (`src/commands/cmd_shell.py`) is an **Infinite Loop** that acts as a traffic controller. It does not "know" commands; it routes them.

### The Routing Logic (Order of Operations)
When you type a command (e.g., `ping`), the Shell follows this strict priority:

1.  **Hardcoded Aliases:** Checks inside `cmd_shell.py` for immediate overrides (like `exit`, `clear`, `exec`).
2.  **Internal Modules:** Checks `src/commands/` for a file named `cmd_ping.py`.
    * *If found:* It imports the module dynamically and runs `run(args)`.
3.  **Magic Commands (JSON):** Checks `data/config/commands.json`.
    * *If found:* It runs the script or alias defined there.
4.  **System Fallback:** If nothing matches, it sends the text to the Host OS (Windows/Linux).

### The Three Modes of Execution
| Mode | Syntax | Description | Use Case |
| :--- | :--- | :--- | :--- |
| **Smart** | `ping google.com` | Tries Internal -> Magic -> System. | 99% of daily use. |
| **Forced** | `exec ping ...` | Bypasses xsv entirely. Forces Host OS to run it. | Testing or conflicts. |
| **Raw** | `cmd` / `sh` | Drops you into the actual OS terminal. | Complex pipes (`|`), heavy admin work. |

---

## 🧩 2. How to Add Features (Modules vs. Scripts)

### Method A: The Python Module (Power User)
**Best for:** Complex tools, interactive menus, API integrations (AI, Web).
1.  Create a file in `src/commands/` named `cmd_YOURNAME.py`.
2.  Paste this template:
    ```python
    def run(args):
        print("This is my new module!")
        # Your python code here
    ```
3.  **Done.** Type `yourname` in the shell.

### Method B: The Magic Script (Quick Fix)
**Best for:** Running a PowerShell/Bash script you found online.
1.  Drop the script into `library/` (e.g., `library/fix_wifi.ps1`).
2.  Open `data/config/commands.json`.
3.  Add it:
    ```json
    "wifi": {
        "type": "script",
        "path": "library/fix_wifi.ps1",
        "description": "Fixes the WiFi adapter"
    }
    ```
4.  **Done.** Type `wifi` in the shell.

---

## ⚡ 3. Aliases (Shortcuts)
Aliases allow you to shorten long commands or complex flags. You define these in `data/config/commands.json`.

### Example 1: Shortening a Command
You want to type `g` instead of `git status`.
```json
"g": {
    "type": "shell",
    "cmd": "git status",
    "description": "Git Status Shortcut"
}

```

### Example 2: Complex Arguments

You want to run a specific Nmap scan by just typing `scan`.

```json
"scan": {
    "type": "shell",
    "cmd": "nmap -sV -p 1-1000 localhost",
    "description": "Run local port scan"
}

```

**Note:** The `commands.json` file is **Hot-Reloaded**. You can save the file and type the command immediately. No restart needed.

---

## ⚠️ Important Rules (Do Not Break These)

1. **Never Edit `src/core/**` unless you are fixing a bug in the engine itself.
2. **Naming Matters:** If you name a module `cmd_ipconfig.py`, you will shadow the Windows `ipconfig` command. (Use `exec ipconfig` to bypass your module).
3. **Keep it Portable:** If writing Python modules, avoid `pip install` dependencies if possible. Use the standard library so it runs on any machine.

```

### 3. What is Next?
You have the Core, the Shell, the Installer, the Settings, and the Documentation.

**We are officially out of the "Infrastructure Phase" and into the "Creative Phase".**

You can now start building the actual tools you wanted:
* `cmd_dev.py` (Install VS Code).
* `cmd_gameserver.py` (Minecraft).
* `cmd_clean.py` (System cleanup).

**Which one do you want to build first?**

```