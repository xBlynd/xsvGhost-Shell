# 🏗️ Ghost Architecture & Rules

## 1. The Interaction Matrix (Touchpoints)

### 🕵️ Stealth Operations
* **Commands:** `ghost cp`, `clean`, `incognito`
* **Engines:** GhostEngine (Hide PID), RootEngine (Wipe Logs), VaultEngine (Store Loot)

### 📡 Network Operations
* **Commands:** `scan`, `ping`, `netmon`
* **Engines:** BlackBoxEngine (Sockets), RootEngine (Raw Packet), InterfaceEngine (Graphs)

### 🔐 Security Operations
* **Commands:** `login`, `lock`, `encrypt`
* **Engines:** SecurityEngine (Auth), GhostCore (Session), InterfaceEngine (Masked Input)

### 📝 Data Operations
* **Commands:** `note`, `journal`, `search`
* **Engines:** VaultEngine (CRUD), SyncEngine (Mirroring), SecurityEngine (Decrypt)

---

## 2. The Core Rules
1.  **No Direct Print:** Engines never print to screen. They return data. Commands print.
2.  **No Direct File Access:** Only `VaultEngine` opens files in `data/vault`.
3.  **No Hardcoded Paths:** All paths must be relative to `ROOT`.
4.  **Manifest Protocol:** Every command MUST have a `MANIFEST` dict for the Help System.

## 3. Folder Map
* `/bin/` -> Portable Python
* `/src/core/` -> The 11 Engines
* `/src/commands/` -> The Interface
* `/data/vault/` -> Encrypted User Data
* `/docs/` -> The Constitution (Public)