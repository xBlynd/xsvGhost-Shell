# Ghost Shell Phoenix v6.5.0 - CHANGELOG

**Codename:** Phoenix - Eve Update  
**Date:** 2026-02-15  
**Approach:** Surgical upgrade on v6.0 foundation (zero breakage)

---

## What Changed (6 files modified, 3 files added)

### NEW FILES
- `src/core/eve_engine.py` (333 lines) — Engine 13: Multi-tier AI integration
  - Replaces the Cortex stub with a functional Ollama integration
  - Tier system: micro (phi3), portable (mistral), mothership (mistral-nemo), cloud (future)
  - Auto-detection of best available tier
  - Shadow loading for USB portability (copies model cache to host temp)
  - stdlib only (urllib.request for HTTP — no `requests` dependency)
  - Conversation history tracking
  - Ghost Shell context injection (Eve knows your OS, role, engines)

- `src/commands/cmd_eve.py` (172 lines) — Full Eve command interface
  - `eve ask <question>` — Query AI with word-wrapped output
  - `eve status` — Show connectivity, tier, Ollama availability
  - `eve tier` — View/set AI tier (auto/micro/portable/mothership)
  - `eve mothership <url>` — Set desktop Ollama URL (Tailscale IP)
  - `eve setup` — Installation guide for Ollama + Tailscale

- `docker-compose.yml` — One-command Ollama deployment
- `data/config/eve.json` — Eve configuration template

### MODIFIED FILES
- `src/core/kernel.py` — Version bumped to 6.5.0-phoenix
  - Boot sequence: `cortex` → `eve` (same slot #13)
  - Codename: "Phoenix - Eve Update"

- `src/core/legion_engine.py` — Upgraded from STUB to OPERATIONAL
  - Version: 0.1.0-stub → 1.0.0
  - `send_message()` now uses HTTP POST (falls back to store-and-forward)
  - `broadcast()` sends to all known nodes
  - NEW: `query_remote_eve()` — Query Eve AI on a remote node
  - NEW: `execute_remote()` — Run commands on remote nodes
  - NEW: `find_mothership()` — Locate the most powerful mesh node
  - References updated: Cortex → Eve throughout

- `src/commands/cmd_ask.py` — Routes to Eve instead of Cortex
- `src/commands/cmd_legion.py` — Status display updated for Phase 1
- `src/commands/cmd_status.py` — Added Eve AI status line to dashboard
- `README.md` — Updated for v6.5 with AI setup instructions

### UNTOUCHED (entire v6 foundation preserved)
- All 11 original engines (ghost_core through sync)
- SecurityEngine (all 348 lines, full key management intact)
- All original commands (help, keys, journal, todo, ping, net, sysinfo, reload, clear)
- Directory structure, data formats, session management
- Compartmentalization doctrine fully maintained

### NOTE
- `cortex_engine.py` still exists on disk as reference material
  but is NOT in the boot sequence (kernel loads eve_engine instead)

---

## Line Count: 3,224 (v6.0) → 3,820 (v6.5) = +596 lines of new functionality
## Engines: 13 (11 original + Legion upgraded + Eve replaces Cortex)
## Commands: 13 (12 original + eve)

---

## Context Preserved From Your Conversations

### From Gemini AI Integration Discussion:
- Mistral-Nemo (12B) for desktop mothership (i7-8700K + RTX 2070)
- Mistral 7B for laptop (ASUS Vivobook + RTX 3050)
- Phi-3 (3.8B) for USB portability
- Tailscale mesh networking for remote AI access
- Shadow loading concept for USB drive protection
- Docker/Ollama deployment strategy

### From Sonnet v7 Attempt (good ideas extracted, bad decisions avoided):
- Eve engine architecture (kept)
- Tier detection system (kept, refined)
- Shadow loading implementation (kept)
- Security engine gutting (REJECTED — kept your full 348-line security)
- Command deletions (REJECTED — kept all 12 original commands)
- Journal rename to "j" (REJECTED — kept journal command)
