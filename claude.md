# CLAUDE.md — Ghost Shell Phoenix Project Constitution
# This file lives in the project root PERMANENTLY. Claude Code reads it automatically.
# Last Updated: 2026-02-17 (Pre-QoL Build)

## Identity

- **Project:** Ghost Shell Phoenix
- **Version:** 6.5.0 (Stable Foundation → QoL Build In Progress)
- **Owner:** Ian Martin (xsvStudio, LLC)
- **Repo:** github.com/xBlynd/xsvGhost-Shell-Phoenix (private)
- **Purpose:** Portable Python-based Life Operating System — personal CLI toolkit, diagnostic weapon, journal, and AI-enhanced command center

## Prime Directives

1. **Portability is Non-Negotiable.** No absolute paths. No registry dependencies. Must run from USB on Windows, Linux, Android (Termux). The Anchor Pattern (`ROOT_DIR = os.path.dirname(...)`) is sacred.
2. **Offline First.** All core features work without internet. Network features are enhancements, not requirements.
3. **Compartmentalization is Sacred.** Engines do ONE job. Failures are isolated. Engines communicate THROUGH the kernel, never import each other directly.
4. **Engines Return Data, Commands Format Display.** Engines return dicts/lists. Commands handle presentation. This lets the owner tweak output without touching engine code.
5. **Silent by Default.** No unnecessary output. No popup windows. Stealth on the host machine.
6. **No Bloat.** stdlib only for core. Optional deps (psutil, cryptography, textual) are graceful-degradation, not hard requirements. No Flask, no Django, no database engines, no GUI libraries.
7. **VaultEngine is the Only Data Gateway.** No command or engine opens data files directly. All data reads/writes go through Vault. If storage backend changes (JSON → SQLite), one file changes.

## Architecture (DO NOT VIOLATE)

### The 13-Engine Grid
```
Engine 01: GhostCore    — Environment detection, node identity, ROOT_DIR, session state
Engine 02: Security     — Authentication, RBAC, key management (god/admin/guest)
Engine 03: Ghost        — Stealth, anti-forensics, cleanup on shutdown
Engine 04: BlackBox     — Network diagnostics, ping with jitter analysis
Engine 05: Root         — Silent subprocess execution, system commands (returns raw data)
Engine 06: Pulse        — Background scheduling, reminders, daemon threads, toast notifications
Engine 07: Vault        — Journals, todos, notes, data persistence (JSON). ONLY data gateway.
Engine 08: Sync         — USB detection, store-and-forward, export/import backups
Engine 09: Interface    — Visual output, themes, banners, formatting (returns strings, never prints)
Engine 10: Loader       — Dynamic command discovery, hot reload, MANIFEST protocol
Engine 11: Heartbeat    — Health monitoring, boot diagnostics, py_compile checks, auto-repair
Engine 12: Legion       — Mesh networking (Phase 1 HTTP operational)
Engine 13: Eve          — AI integration (multi-tier Ollama: phi3/mistral/mistral-nemo)
```

### Boot Sequence
Engines load in order. If one fails, the system continues (except GhostCore and Security which are FATAL).

### Command Resolution Chain (Three-Tier System)
```
1. System Commands   → src/commands/cmd_*.py         (core Ghost Shell)
2. Custom Commands   → src/commands/custom/cmd_*.py   (user-built, follows standard)
3. Library Scripts   → library/*                       (drag-and-drop, any language)
4. Alias             → data/config/commands.json       (magic launcher shortcuts)
5. Host OS Passthrough → fallback to system shell
```

**The Three Tiers Explained:**
- **System Commands:** Core Ghost Shell. Follow MANIFEST. Full engine access. Touch carefully.
- **Custom Commands:** Your personal tools. Same standard as system. Safe to experiment — breakage isolated from core.
- **Library Scripts:** Mercenaries. Any executable (.py, .ps1, .sh, .bat, .js, .exe). Zero integration required. Launcher auto-discovers by filename. If one crashes, shell continues.

**The Promotion Pipeline:**
```
💡 Idea → 📝 Script → 📂 Library (test it) → 🔧 Custom Command (integrate it) → ⚙️ System Command (rare)
```

### Drop-In Command Pattern
```python
# src/commands/cmd_yourcommand.py  OR  src/commands/custom/cmd_yourcommand.py
DESCRIPTION = "What it does"
USAGE = "yourcommand <args>"
REQUIRED_ROLE = "GUEST"  # or ADMIN, GOD
ENGINE_DEPS = ["root", "vault"]  # engines this command needs

def execute(kernel, args):
    # Access engines through kernel — NEVER import engines directly
    # kernel.get_engine("root") for Root engine
    # kernel.get_engine("vault") for Vault engine
    # Return string (printed by shell) or None
    return "Hello from my command!"
```

**For Library Scripts** (no standard required):
- Drop any executable in `library/`
- Type its name (without extension) in the shell
- Launcher finds it and runs it with the correct interpreter
- No engine access. No kernel. No MANIFEST. Just runs.

## Technical Stack

- **Language:** Python 3.8+ (compatibility target)
- **OS Primary:** Windows 11 (PowerShell), with Linux/Android cross-compat
- **Dev Environment:** C:\Dev\Ghost Shell\Ghost-Shell Git Hub\ (local), S:\xsvStudio\Labs\ (USB)
- **AI Local:** Ollama (Docker) — phi3 (USB), mistral (laptop), mistral-nemo (desktop)
- **Networking:** Tailscale VPN mesh for Legion (100.x.y.z addresses)
- **Planning:** Obsidian + Excalidraw (Moriarty Board)
- **Sync:** SyncThing (PC ↔ Laptop ↔ Samsung Galaxy S24 Ultra)
- **TUI (optional):** Textual — graceful fallback if not installed

## Coding Standards

- **Type hints:** Encouraged but not enforced (Python 3.8 compat)
- **Docstrings:** Google style. Every engine and public method.
- **Error handling:** Fail silently, log to Vault. Never crash the kernel for one engine failure.
- **Output formatting:** Engines return data structures (dicts/lists). InterfaceEngine formats them. Commands call Interface then print the result. No direct `print()` in engines.
- **Imports:** Engines receive kernel reference at `__init__`. NEVER import another engine directly.
- **Threading:** Always `daemon=True`. Never block the main input loop.
- **Paths:** Always `pathlib.Path`. Never string concatenation with `/` or `\`. Never hardcoded.
- **Cross-platform:** Check `platform.system()` before OS-specific calls. Always have a fallback.
- **HTTP:** Use `urllib.request` from stdlib. NEVER use `requests` library.

## Data Sync Rules

| Folder | Syncs? | Why |
|---|---|---|
| `data/vault/` | ✅ YES (SyncThing) | Todos, journals, notes. This IS the user's data. |
| `data/config/` | ✅ YES (SyncThing) | Settings, commands.json. Same experience both machines. |
| `data/keys/` | ❌ NEVER | God Key per-machine. Security boundary. Compromise one ≠ compromise all. |
| `data/logs/` | ⚠️ Optional | Diagnostics. Nice to have, not critical. |
| `data/cache/` | ❌ NEVER | Temp files. Machine-specific. Safe to nuke. |
| `data/queue/` | ❌ NEVER | Future Legion offline queue. Machine-specific by design. |
| `data/session/` | ❌ NEVER | Runtime state. Ephemeral per-boot. |

## The "Never Again" List (Lessons Learned)

- [x] NEVER use absolute paths like `C:\Users\Blynd\...` — use ROOT_DIR + relative
- [x] NEVER try to install global npm packages on Windows without checking corepack first
- [x] NEVER mix old version engine files with new version kernel — cascading errors guaranteed
- [x] NEVER do incremental debugging on complex integration issues — provide complete working solutions
- [x] NEVER gut SecurityEngine or remove commands to "simplify" — the 13-engine architecture is sacred
- [x] NEVER rename commands without discussion (journal != j, todo != t)
- [x] NEVER use `requests` library — use `urllib.request` from stdlib for HTTP
- [x] NEVER suggest Docker for things that can run bare-metal
- [x] NEVER continue a long Claude session past 50% context — commit, reset, fresh session
- [x] NEVER start coding without reading this file first
- [x] NEVER open data files directly in commands or engines — ALL data goes through VaultEngine
- [x] NEVER sync `data/keys/` between machines — keys are per-machine security boundaries
- [x] NEVER put formatting/display logic in engines — engines return data, commands format

## File Structure
```
ghost-shell-phoenix/
├── CLAUDE.md              # THIS FILE — project constitution (PERMANENT, COMMITTED)
├── README.md              # Public-facing docs
├── CHANGELOG.md           # Version history
├── docker-compose.yml     # Ollama deployment
├── .gitignore             # Includes session briefs, brainstorm docs, data/*
├── src/
│   ├── main.py            # Entry point (The Anchor)
│   ├── core/
│   │   ├── kernel.py      # The Conductor — orchestrates everything
│   │   ├── ghost_core.py  # Engine 01
│   │   ├── security_engine.py  # Engine 02
│   │   ├── ghost_engine.py     # Engine 03
│   │   ├── blackbox_engine.py  # Engine 04
│   │   ├── root_engine.py      # Engine 05
│   │   ├── pulse_engine.py     # Engine 06
│   │   ├── vault_engine.py     # Engine 07
│   │   ├── sync_engine.py      # Engine 08
│   │   ├── interface_engine.py # Engine 09
│   │   ├── loader_engine.py    # Engine 10
│   │   ├── heartbeat_engine.py # Engine 11
│   │   ├── legion_engine.py    # Engine 12
│   │   └── eve_engine.py       # Engine 13
│   └── commands/
│       ├── cmd_help.py         # System commands (core Ghost Shell)
│       ├── cmd_status.py
│       ├── cmd_todo.py
│       ├── cmd_journal.py
│       ├── cmd_eve.py
│       ├── ... (more system commands)
│       └── custom/             # User-built commands (same standard, isolated)
│           └── (drop cmd_*.py here)
├── library/                    # Drag-and-drop scripts (any language, zero integration)
│   └── (drop .py, .ps1, .sh, .bat, .js here — runs by filename)
├── data/
│   ├── keys/              # Auth keys (NEVER SYNC, gitignored)
│   ├── vault/             # Journals, todos, notes (SYNC via SyncThing)
│   ├── config/            # Aliases, settings, eve.json (SYNC via SyncThing)
│   ├── session/           # Runtime state (ephemeral, never sync)
│   ├── cache/             # Temp data (never sync, safe to nuke)
│   ├── queue/             # Store-and-forward (never sync)
│   ├── logs/              # Diagnostics (optional sync)
│   └── legion/            # Mesh node registry
└── docs/                  # Architecture docs (future: MkDocs source)
```

## Current State (as of v6.5 — QoL Build)

- **Working:** All 13 engines boot. 13 commands operational. Journal, todo, ping with jitter, key management, hot reload, Eve AI (when Ollama running), Legion Phase 1 HTTP.
- **Stable:** Security with passphrase-protected god.key, RBAC hierarchy, silent auth.
- **QoL Build (in progress):** LoaderEngine (full auto-discovery + MANIFEST), HeartbeatEngine (boot diagnostics, py_compile, auto-repair), Root upgrade (raw data methods, safe command tweaking), Host Navigator (ls/cd/open/find), PulseEngine (reminders + toast), SyncEngine (export/import backups), InterfaceEngine (formatting + optional Textual TUI)
- **Planned (NOT building yet):** Full Textual TUI overhaul, Legion Phase 2, Eve architect mode, Ghost Engine stealth suite, Wraith installer, Minecraft server manager

## Session Protocol (For Claude Code / CLI)

1. **Read this file first.** Always. This is non-negotiable.
2. **Three files for a coding session:** `CLAUDE.md` (permanent, in repo), Session Brief (temporary, gitignored), Brainstorm Capture (temporary, gitignored).
3. **Ask clarifying questions** before writing code if the brief is ambiguous.
4. **One feature at a time.** Build, test, confirm, next. Don't boil the ocean.
5. **Test before delivering.** Run `python src/main.py` and verify boot.
6. **Commit checkpoint:** After each working feature, the human commits to git.
7. **Never modify kernel.py boot sequence** without explicit approval.
8. **Never delete existing commands or engines** without explicit approval.
9. **Never continue past 50% context.** Commit what's done, write a handoff summary, start fresh.
10. **End every session with a handoff summary.** What was built, what works, what's next. Save as markdown for the next session.
11. **Be token-efficient.** Claude Code is the expensive phase. Don't explore, don't research, don't brainstorm. Execute the brief. If the brief has holes, say so immediately — don't guess.
12. **Respect the Decision Log.** Decisions below are SETTLED. Do not re-litigate or suggest alternatives unless the human asks.

## Decision Log (SETTLED — Do Not Revisit)

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-02-14 | v6.5 as stable foundation (reject v7 rebuild) | v7 broke everything. Surgical upgrades only. |
| 2026-02-14 | Eve replaces Cortex engine | Multi-tier Ollama approach works |
| 2026-02-14 | Legion upgraded to Phase 1 HTTP | Foundation for mesh before WebSocket/gRPC |
| 2026-02-17 | Textual = optional InterfaceEngine enhancement | Graceful degradation, not hard dependency |
| 2026-02-17 | Obsidian for planning, Ghost Shell for execution | Don't rebuild what Obsidian does better |
| 2026-02-17 | CLAUDE.md + PRD + Session Brief workflow adopted | Boris method, proven process |
| 2026-02-17 | Three-tier command system (system/custom/library) | Promotion pipeline: idea → script → library → command |
| 2026-02-17 | SyncThing for vault/config, NEVER for keys | Security boundary per-machine |
| 2026-02-17 | VaultEngine = only data gateway | Protects future backend migration (JSON → SQLite) |
| 2026-02-17 | Engines return data, commands format display | Owner can tweak output without touching engines |

## For Other AIs Building Ghost Shell Commands

If you are not Claude but are building a command or script for Ghost Shell:
1. Read the Drop-In Command Pattern above
2. For library scripts: just make it work standalone, drop in `library/`
3. For custom commands: follow the pattern, put in `src/commands/custom/`
4. NEVER import engines directly — use `kernel.get_engine("name")`
5. NEVER use absolute paths — use pathlib
6. NEVER use `requests` — use `urllib.request`
7. Test: `python src/main.py` should boot clean with your command showing in `help`
