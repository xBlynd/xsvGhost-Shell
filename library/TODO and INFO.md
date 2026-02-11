# Additional Details and Worklist(Need a better name)
This document goes more into the weeds on individual items for life tracking and fucnitionalility.  This document is the living document.


## "Core or Engine Worklist"
[ ] My Input: We need an ENGINE_API.md. If we update ReminderEngine, how do existing commands know? We need a versioning system for engines so commands don't crash when we upgrade the core.  Status: MISSING.


## Building and Adding to "Ghost Shell"
*Intended to ensure new engines/cores, functions, plugins, commands, scripts or ANYTHING being added follow the requirements of "Ghost Shell" for implementation into ALL items necessary (help menu, info, status, vault, data, security or whatever.)*

### Building Commands
*refer to Building Commands Guide.md as well*
**Help/Info Solution (Drop-In Simplicity)**
```
To get "Drop-In" simplicity + "Crazy" detail, we will use the Self-Contained Manifest pattern.

How it works: Every cmd_*.py file will contain a standard block of text at the top called MANIFEST.

The Magic: You don't edit a central registry. You just drop the file in. The help command automatically scans the file, reads the MANIFEST, and builds the menu dynamically.

The Benefit: A "Crazy Build" can have a 50-line Help Manual inside its own file, and help command will display it perfectly.
```
- Next Steps, Notes and TODOs:
	- Create a "template or example"
	- Requires the completion of Loader Engine.


## 🔐 Security, Login & Obfuscation (The "Ghost" Layer)
User Requirement: "Login and security behind this one... and obfuscation."

You mentioned login in your docs. Currently, cmd_shell.py has a hardcoded admin / admin check. This is not security; it’s a door knocker. If someone opens the Python file, they see the password.

Here is the Real Security Architecture required for a "Professional Field Kit":

### The "Vault Lock" (Encryption): STATUS NOT COMPLETE
The Problem: Your settings.json, email passwords, and journals are sitting in plain text data/vault. If you lose the USB, you lose your identity.

The Fix:

We implement Fernet Encryption (AES-128).

When you run LAUNCH.bat, it asks for a Passphrase.

This passphrase is never stored. It is used to generate a Key in RAM.

This Key decrypts data/vault/secrets.json (where email passwords live) only while the shell is running.

Result: If someone steals the USB, they see encrypted gibberish.

### The Login System (2-Factor / Keyfile) STATUS NOT COMPLETE
The Problem: Typing a password on a hostile computer is dangerous (Keyloggers).

The Fix:

The "Key" File: The USB checks for a specific "License File" or "Key" on the Host Computer (e.g., C:\Users\Ian\xsv_license.key).

If the key exists, it auto-logs in (Trusted Machine).

If not, it demands the Master Password.

### Obfuscation (Hiding the Source) STATUS NOT COMPLETE
The Problem: You said "Obfuscation." Right now, src/core/ is visible code. A client/user could snoop your logic.

The Fix:

Step 1 (Compile): We use Cython or Nuitka to compile your Core Engines (info_engine.py, vault_api.py) into .pyd (DLLs).

Step 2 (Build): We use PyInstaller to wrap the whole thing into xsv.exe.

The Result: The USB contains xsv.exe and an encrypted data/ folder. No .py source code is visible to the user.



## Tools and Utilities or Whatever

### 🛡️ Silent Transfer The "Clean Up" (Anti-Forensics) STATUS NOT COMPLETE
User Requirement: "Silent File Transfer... Wiping traces."

The Problem: Windows logs everything. ShellBags, Prefetch, USB connection logs.

The Fix:

clean Command: This isn't just deleting temp files.

It needs to run wevtutil cl "Windows-System" (Clears Event Logs).

It needs to wipe RecentDocs registry keys.

Timestomping: The ghost cp command we discussed needs to explicitly reset the "Last Access" timestamp of any file it touches so it looks like you were never there.



### 📓 Journal Module (journal)
User Requirement: Date-based logging and searching.

journal (Add entry)

Status: MISSING.

My Input: Needs to auto-append timestamps. [2026-02-10 14:00] User: Entry text.

journal list / journal today / journal view <date>

Status: MISSING.

My Input: The view command needs Pagination. If you have 50 entries for a day, it shouldn't scroll off the screen. It should show 20 lines and ask [More?].

journal search <keyword>

Status: MISSING.

My Input: This is critical. It needs to grep through every .md file in data/vault/journal/ and return: [Date] [Line Number] [Snippet].

journal edit <date>

Status: MISSING.

My Input: Useful for filling in gaps. Should open the full day's log in the system editor.



### 📝Notes Module (note)
User Requirement: Detailed note management.

note add <category> / note view

Status: MISSING (We currently use generic files).

My Input:

Storage: Should be data/vault/notes/[category]/[title].md. Folders are better than tags for portability.

Logic: If the category folder doesn't exist, the engine creates it automatically.

note edit project-x

Status: MISSING.

My Input: This needs to detect the OS. On Windows, it spawns notepad.exe. On Linux, nano or vim. It must verify the file changed after closing to update the "Last Modified" timestamp in our index.

note delete

Status: MISSING.

My Input: Needs a "Trash Can" feature (data/vault/trash/). Never permanently delete immediately. Accidental deletes on a CLI are painful.



### 🖥️ Section 5: Servers (server)
User Requirement: Management of game/app servers.

server install / server list

Status: MISSING.

My Input: We need a server.json catalog. install minecraft should look up the URL in JSON, download the .jar, accepts the EULA automatically, and generate a start.bat.

server backup <name>

Status: MISSING.

My Input: Needs to stop the server (gracefully), zip the folder to data/backups/, and restart the server.