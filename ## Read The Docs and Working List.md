## Read The Docs
- Right now if someone came into the project.  They would be met with a little of a confusing high level readme.  Without knowing the passion of the build and what it is intended to be.  Someone should be able to go into a "Read the Docs" kinda thing(i know python has some).  And get a detailed summary, read mes and how too's on everything.  This is not a task we can complete in one sitting.  But we need to make this a general practice.  Even when we create commands to update a section of "Read the Docs" so people know why the command exists and how it works incase there is other commands of anything that may tie into it, or it breaks with future changes.
- We NEED a VERY clear delination between "CORE" and the rest of EVERYTHING!
- I want it to be so easy, I can tell any dev or AI.  Read this doc and they know exactly how to inject a custom command into the system and it ties into anything it needs or is supposed too.  (Help Menu, Commmands, contains settings, works with core, Help Inspector, if it needs to tie into reminder or the schedule engine, Status, ANYTHING.  We need a LIST)
- Core or Engine Changes.  Same as above.  I want it to be so easy, I can tell any dev or AI.  Read this doc and they know exactly how to inject a custom command into the system and it ties into anything it needs or is supposed too.  (Help Menu, Commmands, contains settings, works with core, Help Inspector, if it needs to tie into reminder or the schedule engine, Status, ANYTHING.  We need a LIST)

## Cross Platform
- Confirm everything is set up running on different devices and operating systems.
- Probably should add a "status" check of some sorts for the "Status Board / Command"
- Confirm this functions in a VM.

## Login and Startup - THIS NEEDS TO BE seperated.  I will want to adjust login screen in future without breaking anything.

- Need a Startup that ties into the Security Check.  After login or signin completed, so a System Info pull and a "status" and sync check or something.

**First run:**
```
╔════════════════════════════════════╗
║    FIRST TIME SETUP - CREATE USER  ║
╚════════════════════════════════════╝

Create username: ian
Create password (min 8 chars): ••••••••••
Confirm password: ••••••••••

[✓] User 'ian' created.
[✓] Ready to use vault.
```

```
╔════════════════════════════════════╗
║      xsv VAULT - SECURE LOGIN      ║
╚════════════════════════════════════╝

Username: ian
Password: ••••••••••

[✓] Authentication successful.
[→] Vault unlocked.
```



## Security
- Login modifications. 
- Security Upgrade in Core / Engine
- Hiding the Code?  When we plug this into a computer, the host machine "could" see all the files and raw code or my private info.  Is there a way to "hide" this entire project?

## Ghost Terminal
- Make it beautiful and clean.


## Vault: Finish or make a Better encryption.... 
- Not even sure we have anything in place yet.



## Core and Portability
[ ] True Portable Python: Currently, LAUNCH.bat relies on the Host Machine having Python installed.
- The Upgrade: We can embed a "Stand-alone Python" folder on the USB stick so this runs on a computer that doesn't have Python installed.

[ ] Gemini AI Hook:
- Context: Mentioned in TODO.md.
- The Upgrade: ask "How do I fix a leaky faucet?" -> Queries Gemini API and prints the answer in the shell.

[ ] The "Setup" Script: You mentioned libnotify-bin for Linux and potentially needing dependencies on Windows.
- The Upgrade: A SETUP.bat / install.sh that detects the host environment and installs missing tools (Git, Python, VS Code) if we are setting up a permanent station.

[ ] USB Autoload / Detection: Listed in TODO.md.
- The Upgrade: When you plug the USB in, can we make it pop a terminal automatically? (Hard on modern Windows, but we can try).

[ ] Sync
- Cloud sync?
- Github syncs?
- Need to seperate this to it doesn't break other things but still syncs everything.
- We need to make sure we have EVERYTHING covered in this sync.  Essientially a "global" list? 

## Status


## Help Menu
	- Want to make a better looking Help Menu.



## Version Control
	- We need better version control and everything.  If the core updates and breaks a command we need to reference versions etc.  Set the standard early.


## HACKER USB and Host (We want to talk about this one......) - Security, Privacy & "The Clean Up" - More Host interaction options.

[ ] Network Monitoring
- Monitoring available in Ghost Terminal or create a new terminal session on Host Machine detached from the "Ghost Shell"
- Have an option to "create" a logging system that we can install on Host PC to monitor and create logs so we can review data.  Example.  There is a persistant issue and we cannot see it right away.  So we need to keep logs to check whats going on throughout the day and night. "This can be used on a variety of "Host" things we build...  
- ADD: Context: You specifically mentioned troubleshooting lag. The Upgrade: A live dashboard command (e.g., netmon) that pings Google/Game Servers continuously and graphs the jitter in the terminal.

[ ] Latency checks

[ ] Check files

[ ] Scan OS files / computer

[ ] Silent File Transfer: 
- Context: Mentioned in TODO.md ("Moving files from work computer to USB untraced"). 
- The Upgrade: A command like ghost cp <target> <dest> that copies files without updating "Last Accessed" timestamps or leaving easy traces.

[ ] The "Cleaner" (Trace Wiper): 
- Current State: repair cleans our internal cache. 
- The Upgrade: A clean command that wipes the Host Machine's Temp files, Browser Cache, and Event Logs before you unplug the stick.

[ ] Kids/Device Monitoring: 
- Context: Mentioned in TODO.md ("Spying/Keylogging to make sure they aren't doing things we don't want"). 
- The Upgrade: Scripts to log active windows or keystrokes on a target machine, saving logs to your Vault.


## 🛠️ The Developer
[ ] Environment Sync (cmd_dev.py): 
- Context: You want to sit at a new PC and have your VS Code settings instantly. 
- The Upgrade: dev sync pulls your extensions list and settings.json from the Vault and applies them to the Host PC.  We want a list of options to install.  Example.  If i am building a webserver, it prompts what kind and downloads and installs everything.  If i need a notepad i probably will pick sublime if its just quick and i dont need to mess with Folders.  We need to think about is one.

[ ] Web Server (cmd_web.py): 
- Context: "Serve" wrapper. The Upgrade: web serve instantly turns the current folder into a LAN-accessible website (great for sharing files locally).

[ ] Network Monitor (Rocket League): 
- Context: You specifically mentioned troubleshooting lag.
- The Upgrade: A live dashboard command (e.g., netmon) that pings Google/Game Servers continuously and graphs the jitter in the terminal.
[ ] Game Server Deployer:
- Context: Minecraft/Ark.
- The Upgrade: game install minecraft -> Downloads server jar, accepts EULA, sets RAM, and launches it from data/servers/.



## Settings - Command Center Settings
	- We need to remember the "Settings Page".  Anything that can have a setting that should change or can change.  Should be integrated into the settings somehow.  This will be helpful with a future dashboard or a webapp or whatever.

## TODO and Task System
[ ] Recurring Tasks: 
- Current State: One-time tasks only. 
- The Upgrade: "Remind me every Friday to check the oil."
[ ] Search:
- Current State: You can list tasks, but not search them.
- The Upgrade: todo search "kids" finds every task or journal entry mentioning "kids".
[ ] Rich Visuals (Color Coding): 
- Current State: All text is default terminal color. 
- The Upgrade: WORK tasks show in Blue, HOME in Green, URGENT in Red.

## Note System - REQUIRES OVERHAUL!!

**Key Changes:**
- No per-line timestamps
- Each "note" can have multiple **entries**
- First entry gets timestamp when created
- Subsequent entries get timestamp when added

**Flow:**

```
>>> note

┌──────────────────────────────────────┐
│  xsv NOTE EDITOR                     │
│  (Type your note. SAVE to finish)    │
└──────────────────────────────────────┘

Note title: Project X - Technical Specs

[2026-02-09 02:15 AM] >>> 
This is my initial note about the project.
I need to implement user authentication.
Also need to handle multi-drive sync.

>>> SAVE

✅ Note saved to: vault/notes/2026-02-09_project-x-technical-specs.md
```

**Later, user adds to same note:**

```
>>> note edit project-x-technical-specs

[Existing Note: Project X - Technical Specs]

Current entries: 1
Last updated: 2026-02-09 02:15 AM

[Options]:
  [1] View current entries
  [2] Add new entry
  [3] Edit existing entry
  [4] Delete entry
  [5] Exit

Choose [1-5]: 2

[ADD NEW ENTRY]
[2026-02-09 11:47 AM] >>>
Started implementation. First pass on auth complete.
Need to test with multiple users.

>>> SAVE

✅ Entry added to: vault/notes/2026-02-09_project-x-technical-specs.md
```

**Note file format (Markdown):**

```markdown
---
title: Project X - Technical Specs
created: 2026-02-09 02:15 AM
last_updated: 2026-02-09 11:47 AM
total_entries: 2
---

### Entry 1 - 2026-02-09 02:15 AM

This is my initial note about the project.
I need to implement user authentication.
Also need to handle multi-drive sync.

---

### Entry 2 - 2026-02-09 11:47 AM

Started implementation. First pass on auth complete.
Need to test with multiple users.

---
```

**Note Commands:**
```
>>> note                          # Create new note
>>> note list                     # List all notes
>>> note view <name>              # View note content
>>> note edit <name>              # Add entry to existing note
>>> note delete <name>            # Delete note
```

***


## Journal - REQUIRES REBUILD!!

[ ] The Journal Viewer: 
- Current State: You have to open the .md files manually. 
- The Upgrade: A journal read command that paginates your entries inside the terminal so you never leave the shell.

**Journal Commands:**
```
>>> journal                        # Add new entry (prompts for date)
>>> journal list                   # Show all journal dates
>>> journal view 2026-02-09        # View specific date's entries
>>> journal today                  # View today's entries
>>> journal search <keyword>       # Search across all journals
>>> journal edit 2026-02-09        # Add another entry to existing date
```



## Commands  (THIS IS NOT THE FULL LIST - IANS WORKING IDEAS OR LIST)


```
=== AUTHENTICATION ===
login                               # Login on startup (automatic)
security                            # Manage security settings
security enable_bitlocker?           # Enable BitLocker? encryption
security change_password            # Change vault password

=== NOTES ===
note                                # Create new note
note list                           # List all notes
note view project-x-technical      # View note content
note edit project-x-technical      # Add new entry to note
note delete project-x-technical    # Delete note

=== JOURNAL ===
journal                             # Add journal entry (prompts for date)
journal list                        # List all journal dates
journal today                       # View today's entries
journal view 2026-02-09            # View specific date
journal search deployment          # Search all journals
journal edit 2026-02-09            # Add entry to existing date


=== SERVERS ===
server install                      # Install new game server
server list                         # List active servers
server backup <name>               # Backup server

=== COMMANDS & SCRIPTS ===
list                                # List available commands
run mmand>                       # Run command/script
wizard                              # Create new custom command

=== SYNC & BACKUP ===
sync list                          # List connected drives
sync merge <drive>                 # Merge vaults
sync status                        # Check sync status

=== EMAIL (Future) ===
email                              # Email client menu
email config                       # Configure IMAP
email check                        # Check mail

=== UTILITY ===
help                               # Show all commands
about                              # About xsvStudio Vault
exit                               # Exit vault
```