# 👻 Ghost Shell Phoenix v6.5

**"One Stick, Any Computer, Surgical Precision"**

A portable Python-based Life Operating System. Modular command shell that works from USB on any machine.
Now with Eve AI integration and operational Legion mesh networking.

## Quick Start

```bash
python src/main.py          # Boot Ghost Shell
python src/main.py --debug  # Verbose boot logging
```

On first boot, you'll be prompted to create your God Key (master passphrase).

## AI Setup (Optional)

```bash
# Install Ollama (https://ollama.ai)
ollama pull mistral          # 7B model for local AI
# Then in Ghost Shell:
eve ask "Hello, are you working?"
eve status                   # Check AI connectivity
```

## Core Commands

| Command | Description |
|---------|-------------|
| `help`     | Show all available commands |
| `status`   | System health dashboard |
| `ping`     | Enhanced ping with jitter analysis |
| `journal`  | Personal journal management |
| `todo`     | Task management |
| `keys`     | Authentication key management |
| `net`      | Network tools |
| `sysinfo`  | Host system information |
| `reload`   | Hot reload commands without restart |
| `ask`      | Quick AI query (routes to Eve) |
| `eve`      | Full Eve AI interface (ask, status, tier, setup) |
| `legion`   | Mesh network management |

Any unrecognized command passes through to the host OS shell.

## Architecture

13 engines orchestrated by a central kernel:

| # | Engine | Role |
|---|--------|------|
| 01 | Ghost Core | Environment detection, node identity |
| 02 | Security | Authentication, RBAC, key management |
| 03 | Ghost | Stealth, cleanup |
| 04 | BlackBox | Network diagnostics |
| 05 | Root | Silent system execution |
| 06 | Pulse | Background scheduling (daemon threads) |
| 07 | Vault | Journals, todos, data persistence |
| 08 | Sync | USB sync, store-and-forward |
| 09 | Interface | Visual output, themes |
| 10 | Loader | Dynamic command discovery, hot reload |
| 11 | Heartbeat | Health monitoring |
| 12 | Legion | Distributed mesh (Phase 1 - HTTP) |
| 13 | Eve | AI integration (Ollama/Tailscale) |

## Adding Commands

Drop a `cmd_yourcommand.py` file into `src/commands/`:

```python
DESCRIPTION = "What it does"
REQUIRED_ROLE = "GUEST"  # or ADMIN, GOD

def execute(kernel, args):
    return "Hello from my command!"
```

It's auto-discovered on boot. Use `reload yourcommand` to update without restarting.

## Key System

- **God Key**: Full access. Created on first boot.
- **Admin Key**: Standard access. Issued via `keys issue admin`
- **Guest Key**: Read-only. `keys issue guest 24h "Friend's laptop"`

## Project Structure

```
ghost-shell/
├── src/
│   ├── main.py              # Entry point
│   ├── core/
│   │   ├── kernel.py         # The conductor
│   │   ├── ghost_core.py     # Engine 01-13...
│   │   └── ...
│   └── commands/
│       ├── cmd_help.py       # Drop-in commands
│       └── ...
├── data/
│   ├── keys/                 # Authentication keys (gitignored)
│   ├── vault/                # Journals, todos
│   ├── config/               # Aliases, settings
│   └── session/              # Runtime state
└── docs/                     # Architecture docs
```

## Requirements

- Python 3.8+
- No external dependencies for core (stdlib only)
- Optional: `psutil` for memory monitoring

## Philosophy

1. **Compartmentalization is sacred** - engines fail in isolation
2. **Offline first** - core works without internet
3. **Portable is non-negotiable** - no absolute paths
4. **Silent by default** - no unnecessary output
5. **Extensible through simplicity** - drop-in commands, hot reload

## License

Private project.
