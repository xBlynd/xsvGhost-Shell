# Building Command Guide

## Drop-In Commands (NO COMPLETE)

**Help/Info Solution (Drop-In Simplicity)**
```
To get "Drop-In" simplicity + "Crazy" detail, we will use the Self-Contained Manifest pattern.

How it works: Every cmd_*.py file will contain a standard block of text at the top called MANIFEST.

The Magic: You don't edit a central registry. You just drop the file in. The help command automatically scans the file, reads the MANIFEST, and builds the menu dynamically.

The Benefit: A "Crazy Build" can have a 50-line Help Manual inside its own file, and help command will display it perfectly.
```
- Next Steps and Notes:
	- Create a "template or example"
	- Requires the completion of Loader Engine.



### 2. The Engine-by-Engine Interaction Guide

*If you are building a Command, here is who you need to talk to.*

#### 💀 1. GhostCore (The Environment)

* **The Touchpoint:** The "God Object."
* **When to touch it:**
* You need a setting (e.g., `user_color`).
* You need to know if you are on Linux or Windows.
* You need the path to the Portable Python binary.


* **The Flow:** `Command -> GhostCore -> Config File`

#### 🛡️ 2. SecurityEngine (The Crypto-Layer)

* **The Touchpoint:** The Wrapper.
* **How it talks:** It wraps around the **VaultEngine**. You rarely call Vault directly for sensitive data; you call Security, which unlocks Vault.
* **When to touch it:**
* You are saving a password.
* You are accessing `data/vault/loot/`.
* You want to lock the terminal manually.



#### 👻 3. GhostEngine (The Stealth Wrapper)

* **The Touchpoint:** The Modifier.
* **How it talks:** It talks extensively to **RootEngine** (to hack the system) and **VaultEngine** (to modify file timestamps).
* **When to touch it:**
* Your command is about to do something loud (e.g., network scan). You call `Ghost.enable_stealth()` first.
* You just saved a file to the Host. You call `Ghost.timestomp(path)` to make it look old.



#### 📡 4. BlackBoxEngine (The Network)

* **The Touchpoint:** The Pipe.
* **How it talks:** It functions almost independently but logs data to **VaultEngine** (CSV logs).
* **When to touch it:**
* You need to ping something.
* You need to download a file without using a Browser.



#### ⚡ 5. RootEngine (The Hands)

* **The Touchpoint:** The Weapon.
* **How it talks:** This is the *only* engine allowed to use `ctypes` or `sudo`. **GhostEngine** relies heavily on this.
* **When to touch it:**
* You need to kill a specific PID.
* You need to change a Registry Key.
* **WARNING:** If `GhostCore` says we are on Linux, RootEngine behaves differently than on Windows.



#### 📚 7. VaultEngine (The Storage)

* **The Touchpoint:** The Hard Drive.
* **How it talks:** It is the *only* engine allowed to use `open()`.
* **When to touch it:**
* You are saving a Note, Journal, or Log.
* **Rule:** If the data is sensitive, you must pass `encrypted=True`, which triggers a handshake with **SecurityEngine**.



#### 📺 9. InterfaceEngine (The UI)

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