# Ghost Shell Folder and Filing Structure and Mapping The "Living Document"
*All Folders or housing or whatever are to be monitired in the "Ghost Shell Status" to be monitored in the "Status Menu"*
*Atlas is to be available upon a about or info command is run in the "Ghost Shell"*
*Master Document located in "Ghost Shell" Document Library*

**Ghost Shell Folder and File Structure**
*this section contains the maping of the way our "Ghost Servers" Folder structure is laid out.*
*each folder has a desription of what it is and why*
*this section also has a "touch point" map that visually helps understand how each core and engine touch each section. (also how the commands and scripts, etc)*


## 1. 📂 Ghost Shell Directory Map

### 1. The Root (`/`)
* `LAUNCH.bat` / `xsv.sh`: The Keys to the car.
* `README.md`: The public cover story.
* `bin/`: **Portable Python Runtime** (Managed by GhostCore).

### 2. The Source (`src/`)
* `core/`: **The 11 Engines** (GhostCore, BlackBox, Vault, etc.).
* `commands/`: **The Interface Layer** (The scripts you type).
* `main.py`: The Entry Point (The Router).

### 3. The Constitution (`docs/`) [Public]
* `SYSTEM_ATLAS.md`: The Engine Map (This document).
* `COMMAND_API.md`: The Template for creating new tools.
* `ARCHITECTURE.md`: The Rules of Engagement.

### 4. The Data Center (`data/`)
* `config/`: **System Settings** (settings.json, commands.json).
* `logs/`: **BlackBox Logs** (Jitter.csv, network_trace.log).
* `servers/`: **Game Servers** (Minecraft .jars, Ark configs).

### 5. The Vault (`data/vault/`) [Encrypted/Private]
* `keys/`: **SecurityEngine** keyfiles (Never synced to Git).
* `journal/`: Your daily logs (`VaultEngine`).
* `notes/`: Your project notes (`VaultEngine`).
* `library/`: **The Life Archive** (PDFs, Manuals, Receipts).
* `loot/`: **The Drop Zone** (Files stolen/copied via `ghost cp`).


## 2. The "Document Library" and How it works?

*Where do the docs live?*
Strict separation between **Technical Manuals** (for the code) and **Your Life Library** (for you), but they must both be searchable.

* **`docs/` (The Constitution):**
* **Public.** Contains `ARCHITECTURE.md`, `COMMAND_API.md`.
* *Purpose:* If you hand this USB to a dev, they read this to know how to code.


* **`data/vault/library/` (The Life Archive):**
* **Private/Encrypted.** Contains your PDF manuals, car insurance, scanned receipts.
* *Purpose:* Your "Second Brain."


* **`data/vault/loot/` (The Drop Zone):**
* **Private/Encrypted.** Where `ghost cp` dumps stolen/copied files.



**The Search Vision:** eventually, a command like `search "insurance"` will check **BOTH** the `docs/` folder (for code help) and `data/vault/library/` (for your life docs).



## 3. 🗺️ The Component Map

* **Where is the Installer?**
* **Location:** Root folder (`/install.bat` or `/setup.sh`).
* **Managed By:** It is a standalone script that calls **`GhostCore`** to initialize the environment.


* **Where is Python held?**
* **Location:** `/bin/python/` (On the USB Stick).
* **Managed By:** `LAUNCH.bat` points to this folder so we don't rely on the Host OS.


* **Where are "Ghost Shell Settings"?**
* **Location:** `data/config/settings.json`.
* **Managed By:** **`GhostCore`** loads them, but **`InterfaceEngine`** provides the `settings` command to edit them.


* **Where is the "Ghost Shell" Appearance?**
* **Location:** **`InterfaceEngine`**. It controls the colors, the ASCII art, and the prompt style.


* **Document Drag & Drop?**
* **Location:** **`VaultEngine`**. It watches `data/vault/library`. If you drop a file there, it indexes it for Search.


* **Syncing Core vs. Private?**
* **Location:** **`SyncEngine`**. It has two profiles:
* `Profile A (System)`: Syncs `src/` (The Code) to GitHub.
* `Profile B (Soul)`: Syncs `data/vault/` (The Data) to your Private Cloud/USB.




## 4. The Visual Command Map ( NOT CURRENT and looks like SHIT)


| Engine | Associated Commands |
| --- | --- |
| **GhostCore** | `setup`, `info`, `exit` |
| **Security** | `login`, `lock`, `encrypt`, `decrypt` |
| **Ghost (Stealth)** | `ghost cp` (Silent Copy), `clean` (Wipe Traces) |
| **BlackBox** | `scan`, `ping`, `netmon`, `incognito` |
| **Root** | `kill`, `tune`, `sysinfo` |
| **Pulse** | `remind`, `schedule`, `timer` |
| **Vault** | `note`, `journal`, `search`, `library` |
| **Sync** | `sync`, `backup`, `restore` |
| **Interface** | `help`, `clear`, `theme`, `alias` |
| **Loader** | `create` (Wizard), `reload` |
| **Heartbeat** | `status`, `repair` |





## 5. 🕸️ The Ghost Touchpoint Map

### The Interaction Matrix

This table visualizes "Who talks to Who."

* **Rows:** The Engine doing the work.
* **Columns:** Who relies on it.

| Engine | Used By (Upstream) | Dependencies (Downstream) | Critical Hooks / "Touchpoints" |
| --- | --- | --- | --- |
| **1. GhostCore** | *EVERYONE* | OS, FileSystem | `config.get()`, `os_is_linux()` |
| **2. Security** | Vault, Interface, Ghost | GhostCore | `decrypt()`, `verify_key()`, `lock_session()` |
| **3. Ghost (Stealth)** | Root, Interface | RootEngine | `hide_pid()`, `timestomp()`, `wipe_trace()` |
| **4. BlackBox** | Interface, Pulse | RootEngine | `socket_connect()`, `log_jitter()`, `spoof_header()` |
| **5. Root** | Ghost, BlackBox | *Host OS API* | `registry_write()`, `kill_proc()`, `get_hwid()` |
| **6. Pulse** | Interface, Loader | GhostCore | `notify()`, `parse_relative_time()`, `schedule()` |
| **7. Vault** | Sync, Interface, Loader | Security, GhostCore | `save_note()`, `get_json()`, `search_index()` |
| **8. Sync** | Interface | Vault, Security | `mirror_drive()`, `resolve_conflict()` |
| **9. Interface** | *User* | *All Engines* | `print_formatted()`, `ask_user()`, `register_alias()` |
| **10. Loader** | Interface | GhostCore | `load_command()`, `check_deps()` |
| **11. Heartbeat** | *System Loop* | *All Engines* | `verify_hash()`, `log_crash()` |

---

## 6. The Engine-by-Engine Interaction Guide

*If you are building a Command, here is who you need to talk to. Referenced on @Building Commands Guide.md*

### 💀 1. GhostCore (The Environment)

* **The Touchpoint:** The "God Object."
* **When to touch it:**
* You need a setting (e.g., `user_color`).
* You need to know if you are on Linux or Windows.
* You need the path to the Portable Python binary.


* **The Flow:** `Command -> GhostCore -> Config File`

### 🛡️ 2. SecurityEngine (The Crypto-Layer)

* **The Touchpoint:** The Wrapper.
* **How it talks:** It wraps around the **VaultEngine**. You rarely call Vault directly for sensitive data; you call Security, which unlocks Vault.
* **When to touch it:**
* You are saving a password.
* You are accessing `data/vault/loot/`.
* You want to lock the terminal manually.



### 👻 3. GhostEngine (The Stealth Wrapper)

* **The Touchpoint:** The Modifier.
* **How it talks:** It talks extensively to **RootEngine** (to hack the system) and **VaultEngine** (to modify file timestamps).
* **When to touch it:**
* Your command is about to do something loud (e.g., network scan). You call `Ghost.enable_stealth()` first.
* You just saved a file to the Host. You call `Ghost.timestomp(path)` to make it look old.



### 📡 4. BlackBoxEngine (The Network)

* **The Touchpoint:** The Pipe.
* **How it talks:** It functions almost independently but logs data to **VaultEngine** (CSV logs).
* **When to touch it:**
* You need to ping something.
* You need to download a file without using a Browser.



### ⚡ 5. RootEngine (The Hands)

* **The Touchpoint:** The Weapon.
* **How it talks:** This is the *only* engine allowed to use `ctypes` or `sudo`. **GhostEngine** relies heavily on this.
* **When to touch it:**
* You need to kill a specific PID.
* You need to change a Registry Key.
* **WARNING:** If `GhostCore` says we are on Linux, RootEngine behaves differently than on Windows.



### 📚 7. VaultEngine (The Storage)

* **The Touchpoint:** The Hard Drive.
* **How it talks:** It is the *only* engine allowed to use `open()`.
* **When to touch it:**
* You are saving a Note, Journal, or Log.
* **Rule:** If the data is sensitive, you must pass `encrypted=True`, which triggers a handshake with **SecurityEngine**.



### 📺 9. InterfaceEngine (The UI)

* **The Touchpoint:** The Canvas.
* **How it talks:** Commands use this to print.
* **When to touch it:**
* Don't use `print()`. Use `Interface.print_success()` or `Interface.print_error()`.
* This ensures the colors match the current Theme defined in **GhostCore**.



---

### 3. Example Workflow: "The Silent Copy"

*Visualizing how a single command (`ghost cp`) touches 5 different Engines.*

1. **User** types: `ghost cp C:\Passwords.txt`
2. **LoaderEngine** finds `cmd_ghost.py` and runs it.
3. **Command** calls **GhostEngine** -> `initiate_transfer()`.
4. **GhostEngine** calls **RootEngine** -> `read_file_raw()` (Bypassing locks).
5. **GhostEngine** calls **SecurityEngine** -> `encrypt_stream()`.
6. **SecurityEngine** calls **VaultEngine** -> `save_to_loot()`.
7. **GhostEngine** calls **RootEngine** -> `timestomp_host_logs()` (To hide the read event).
8. **InterfaceEngine** -> `print_success("Asset Acquired")`.

---

