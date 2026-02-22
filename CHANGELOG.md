# Ghost Shell Phoenix — Changelog

> One file, newest first. Every commit that adds a feature gets a line here.
> Feature branches add their own section before merge — no changelog work at merge time.

---

## [v6.5.0-post-qol] — 2026-02-22

Ghost Drive architecture documentation + Minecraft world backup command.

### Added
- `src/commands/custom/cmd_mc.py` — Minecraft world backup command
  - Back up, restore, and list Minecraft saves to `data/vault/mc_backups/`
  - Supports named backups with timestamps, restore by name, compressed archives
- `docs/GHOST_DRIVE_VISION.md` — Ghost Drive portable deployment architecture doc
  - Three deployment modes: USB Ghost, Installed Node, EXE
  - Threat model, build roadmap (Phases A–D), TODO gaps marked for Ian to fill
  - Ghost Engine stealth suite design, Wraith installer concept
- Kernel file-transfer support additions (supporting mc backup transport)

### Updated
- `CLAUDE.md` — Ghost Drive section added, pointing to vision doc and build status
  - Build phases A–D documented as NOT YET STARTED pending vision doc completion

---

## [v6.5.0-qol] — 2026-02-18

QoL Build: 7 engine upgrades, 7 new commands, 20 total commands operational.

### Engine Upgrades (all bumped to v2.0.0)
- **LoaderEngine v2** — Full auto-discovery, MANIFEST protocol, hot reload, validation
- **HeartbeatEngine v2** — Boot diagnostics, `py_compile` checks, auto-repair, health scoring
- **RootEngine v2** — Raw data methods, structured output for `ipconfig /all`, safe command wrapper
- **PulseEngine v2** — Reminder scheduling, daemon threads, VBS toast notifications (Windows)
- **VaultEngine v2** — Unified data gateway, atomic writes, backup rotation
- **SyncEngine v2** — USB detection, store-and-forward, export/import backups
- **InterfaceEngine v2** — Theme system, banner formatting, structured output helpers

### New Commands (7)
- `netinfo` — Structured network adapter info (IP, MAC, gateway, DNS per adapter)
- `cleanup` — Ghost cleanup: logs, cache, session files, orphaned temp data
- `host` — Host navigator: `ls`, `cd`, `open`, `find` for host filesystem browsing
- `remind` — Reminder management: set, list, cancel timed reminders via PulseEngine
- `sync` — Backup export/import, USB sync status via SyncEngine
- `config` — Live config viewer/editor for `data/config/commands.json`
- `dashboard` — System health overview: boot status, engine grid, reminder queue, todo count

### Existing Commands Updated
- All 13 original commands updated with MANIFEST dicts
- `ask`, `clear`, `eve`, `help`, `journal`, `keys`, `legion`, `net`, `ping`, `reload`, `status`, `sysinfo`, `todo`

### Total: 20 commands operational

> Full session detail: `SESSION_REPORT_2026-02-18.md` (gitignored, local archive)

---

## [v6.5.0-phoenix] — 2026-02-15

Eve AI engine (Engine 13), Legion Phase 1 HTTP mesh, TUI entry screen foundation.

### Added
- **Engine 13: EveEngine** — Multi-tier Ollama AI integration
  - Model tiers: phi3 (USB/portable), mistral (laptop), mistral-nemo (desktop)
  - Graceful degradation when Ollama not running
  - `ask` and `eve` commands wired to EveEngine
- **Legion Phase 1 HTTP** — Mesh networking upgraded from stub to operational
  - HTTP node-to-node communication (100.x.y.z Tailscale addresses)
  - Node registry, store-and-forward queue foundation
  - `legion` command for mesh status and node management
- **TUI entry screen foundation** — `src/tui/` scaffolding (Textual, optional dep)
- `cmd_net.py` — Network status command using BlackBoxEngine
- `cmd_ping.py` — Ping with jitter analysis

### Architecture
- 13-engine grid fully populated
- Three-tier command system formalized (system / custom / library)
- VaultEngine established as sole data gateway
- Security RBAC hierarchy: god / admin / guest with passphrase-protected god.key

> Full detail preserved in: `2026-02-15-changelog_v6.5.0.md` (historical archive, do not edit)
