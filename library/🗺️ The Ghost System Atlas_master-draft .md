### 🗺️ The Ghost System Atlas (Revised)
*All Engines and Cores to be monitored in the "Status Menu"*
*Atlas is to be available upon a about or info command is run in the "Ghost Shell"*
*Master Document located in "Ghost Shell" Document Library*

#### 1. 👻 The GhostCoreEngine (The Kernel)

* **Role:** The Brain & Environment Detector.
* **Scope:** The first thing that wakes up. It determines *where* we are (Windows/Linux) and loads the config.
* **Passion:** "The Awakening. It creates the reality in which the Ghost exists, bridging the gap between dead silicon and our living code."
* **Responsibilities:**
* **OS Detection:** Instantly identifies Host OS (Debian/Arch/Windows) and sets the `IS_LINUX` flag for other engines.
* **Config Loader:** Reads `data/config/settings.json` and distributes preferences to all engines.
* **Dependency Check:** Verifies if Python, Node, or `libnotify` are installed on the Host.


#### 2. 🛡️ The SecurityEngine (The Gatekeeper)

* **Role:** Defense & Authentication.
* **Scope:** Keeps *our* data safe. This is separate from "Hacking" tools.
* **Passion:** "Invisibility is our armor. We operate in the shadows, leaving no trace but the results."
* **Responsibilities:**
* **Login System:** Manages the startup password, Keyfile checks, and 2FA.
* **The Vault Key:** Holds the Fernet Encryption Key in RAM (never on disk) to read/write secure files.
* **Session Monitor:** Auto-locks the shell if you are idle for 5 minutes.


#### 3. 👻 The GhostEngine (The Phantom)

* **Role:** Offensive Stealth & Anti-Forensics.
* **Scope:** **"Hack the Box"** tools. Zero Footprint operations.
* **Passion:** "Knowledge is power. We see everything; they see nothing."
* **Responsibilities:**
* **Active Stealth:** "Ghost Mode" - Hooks into the Host OS to hide our process ID (PID) from Task Manager. PID Spoofing and more.
* **Ghost Mode:**
* **Anti-Forensics:** Timestomping (resetting file access times), wiping `ShellBags`, scrubbing the Clipboard.
* **Payload Delivery:** The logic to inject scripts or tools into the Host without triggering Windows Defender (using PowerShell reflection), Linux or Debian. Loading scripts into RAM without touching the hard drive.
* **The "Key":** Manages the Fernet Encryption that keeps your Vault locked.
* **Trace Wiper:** The "Clean" command logic (Wiping Temp/RecentDocs on exit).



#### 4. 📡 The BlackBoxEngine (The Shadow Network)

* **Role:** The Shadow Network. Network Dominance & Forensics.
* **Scope:** Total network dominance and anonymity. Analysis, Anonymity, and Attack.
* **Passion:**
* **Responsibilities:**
* **Incognito Search:** A headless browser engine (or curled requests) that spoofs User-Agents and proxies traffic to query Google/Perplexity without leaving a browser history trail.
* **Traffic Intercept:** Promiscuous mode scanning (Seeing what IoT devices/users are on the wifi).
* **Jitter/Lag Forensics:** The deep logging you wanted for (Packet loss variance, hop-by-hop analysis), internet provider troubleshooting, router, modem, etc. Analysis, Anonymity, and Attack. Logging packet loss variance to CSV for troubleshooting.
* **Tunneling:** Creating reverse SSH tunnels to "phone home" from a restricted network. managing SSH
* **Promiscuous Mode:** Scanning the local subnet for IoT devices and users.


#### 5. ⚡ The RootEngine (The Mechanic)

* **Role:** Host Control / God Mode.
* **Scope:** Absolute control over the Host Machine's hardware and settings.
* **Passion:** The bridge between our Ghost world and the Host machine.
* **Responsibilities:**
* **System Tuning:** Registry hacks to optimize TCP/IP settings, disable telemetry, or debloat Windows.
* **Process Termination:** Not just `kill`, but `force kill` that suspends the thread first (anti-malware style).
* **Hardware ID:** Spoofing or reading HWIDs (Motherboard serials, MAC addresses, etc...).
* **User Management:** Enabling/Disabling accounts, resetting local passwords (if we have admin).


#### 6. ⏳ The PulseEngine (The Timekeeper)

* **Role:** Scheduling & Consciousness.
* **Scope:** Precision scheduling and any future responsibilties. Making the shell "alive" and aware of time.
* **Passion:** A system without time is dead. The PulseEngine makes the shell "conscious" of the clock.
* **Responsibilities:**
* **The Scheduler:** Executing cron-style jobs "Run clean.py every 10 minutes."
* **Relative Time:** Parsing "10m", "2h", "next friday".
* **Toast Notifications:** Handling and Dispatching visual alerts to Windows/Linux.


#### 7. 📚 The VaultEngine (The Librarian)

* **Role:** Data Management.
* **Scope:** The **ONLY** way to read/write `data/vault`.
* **Passion:** Data hygiene is next to godliness. This engine ensures no file is ever corrupted, lost, or misplaced.
* **Responsibilities:**
* **CRUD:** Create, Read, Update, Delete logic for Notes and Journals and other documents.
* **Search Index:** `grep` logic to find keywords across all markdown files.
* **Structure Repair:** Recreating folders (`notes`, `loot`, `library`) if they are deleted.
* **Encryption Hook:** Uses `SecurityEngine` to decrypt files on the fly.


#### 8. 🔄 The SyncEngine (The Bridge)

* **Role:** Data Transport.
* **Scope:** Moving data between the USB, the Host, and the Cloud.
* **Passion:** "Ubiquity. We are everywhere and nowhere at once, ensuring the Soul survives even if the body is lost."
* **Responsibilities:**
* **Mirroring:** One-way sync (Vault -> Host or Host -> Vault).
* **Silent Transfer:** The `ghost cp` logic (Copying files without updating timestamps).
* **Conflict Resolution:** Handling what happens when two files have the same name.


#### 9. 📺 The InterfaceEngine (The Face)

* **Role:** UI, Help, and Alias Manager.
* **Scope:** How the user interacts with the system.
* **Passion:** "Control. Infinite power presented with elegant simplicity."
* **Responsibilities:**
* **Help Generator:** Dynamically building the Help Menu from command manifests.
* **Alias Manager:** Handling shortcuts (e.g., `p` = `ping`).
* **Theming:** Managing colors/prompts (Blue for Work, Red for Root).
* **Spinner/Loader:** Showing "Working..." animations during long tasks.


#### 10. 🧩 The LoaderEngine (The Nervous System)

* **Role:** Expansion & routing.
* **Scope:** Loading commands from files. Infinite Expansion.
* **Passion:** Infinite expansion without bloat. It allows us to drop a file in a folder and have it "come alive" instantly.
* **Responsibilities:**
* **Hot-Swap:** Detecting new commands and scripts from the library instantly.
* **Manifest Parsing:** Reading the metadata (Help Text, Version, Author) of a command. And before loading it.
* **Dependency Check:** Ensuring a command has the tools it needs to run.  "This command requires `nmap`. Is `nmap` installed? No? Alert user."



#### 11. 💓 The HeartbeatEngine (The Immune System)

* **Role:** Vital Signs & Diagnostics.
* **Scope:** Ensuring *our* existence and the shell itself is healthy.
* **Passion:** A broken tool is worse than no tool. This engine constantly checks if the system is healthy.
* **Responsibilities:**
* **Self-Healing:** Detecting corrupted core files and restoring them. If `RootEngine` is deleted, this engine rebuilds it from a backup.
* **Integrity Pulse:** Constantly checking file hashes to ensure no one has tampered with our code.
* **Crash Handler:** If a module fails, this catches the error and logs it to `data/logs/crash.log` instead of killing the shell.
* **Engine and Core Monitoring:** Monitor all engines and cores.  Information to be include the "status" commands.
* **Vault Monitoring** - Monitor the status of EVERYTHING vault.
* **Ghost Monitoring** - Monitor Ghost and Rogue Modes
* **Shadow Monitoring** - Monitor all shadow actions done with the Blackbox items.





### NOTES AND/OR COMMENTS
- I want to have a map for the commands and under which item(engine or core) it is held or derives from.  Think this will help me and other visually see whats happening too.

###  ORGANIZE UNDER OR CREATE ENGINES
- I want to have a map for the commands and under which item it is held or derives from.
- Installer, where are we located and how is this managed?
- Loaders screens(Pre-loaders, Login, system startup, etc)
- The "Ghost" Shell itself.  And its appearance, do we keep that in the same location or seperate into interface?
- Our python, where is that held at?
- "Ghost Shell Settings" - Where does this fall under and how do we make sure all the engines settings get into this as well?
- Document library and handling me draging ANY file i want into my document library and the system knowing it.
- Syncing the "core" vs the "private files needs to be identified somewhere."