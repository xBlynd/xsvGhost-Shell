# Ghost Shell Phoenix v6.5.0

**"One Stick, Any Computer, Surgical Precision"**

Ghost Shell is a portable, modular, Python-based Life Operating System designed to run from a USB drive on any host machine (Windows, Linux, macOS) without leaving a trace. It features a micro-kernel architecture, mesh networking (Legion), and local AI integration (Eve).

## Architecture

The system is built around a central **Kernel** (`src/core/kernel.py`) that orchestrates **13 Engines**.

### Core Engines
1.  **Ghost Core:** Environment detection and identity.
2.  **Security:** RBAC, key management, and authentication.
3.  **Heartbeat:** Health monitoring and diagnostics.
4.  **Loader:** Dynamic command and library discovery.
5.  **Root:** System-level execution (silent).
6.  **Pulse:** Background task scheduling.
7.  **Vault:** Data persistence (journals, todos).
8.  **Interface:** TUI, themes, and user interaction.
9.  **BlackBox:** Network diagnostics.
10. **Ghost:** Stealth and cleanup operations.
11. **Sync:** USB synchronization and store-and-forward.
12. **Legion:** Distributed mesh networking (HTTP/Tailscale).
13. **Eve:** Local AI integration (Ollama).

### Key Concepts
*   **Compartmentalization:** Engines must fail in isolation. One crashing engine should not take down the kernel.
*   **Portability:** The system must run on *any* host OS. Absolute paths are forbidden; usage of `ROOT_DIR` anchor is mandatory.
*   **Zero-Dependency Core:** The core system relies exclusively on the Python Standard Library to ensure it runs on any machine with Python installed. External libraries (like `requests`) are avoided in favor of `urllib` for core functions.
*   **Security:** Access is controlled via "God", "Admin", and "Guest" keys.

## Development Workflow

### Booting the Shell
```bash
# Standard Boot
python src/main.py

# Debug Mode (Verbose logging)
python src/main.py --debug

# Headless Mode (Automation/Server)
python src/main.py --headless
```

### Creating Commands
Refer to `COMMAND_STANDARD.md` for detailed protocols.

1.  **Library Scripts (`library/`):** Standalone scripts (Python, Bash, PowerShell) runnable via the shell. No kernel access.
2.  **Custom Commands (`src/commands/custom/`):** Integrated Python modules with full Kernel/Engine access.
3.  **System Commands (`src/commands/`):** Core functionality. Modify with extreme caution.

**Command Template:**
```python
MANIFEST = {
    "name": "mycmd",
    "description": "Does something cool",
    "version": "1.0.0",
    "usage": "mycmd <args>",
    "required_role": "GUEST", # or ADMIN, GOD
    "engine_deps": ["vault"]
}

def execute(kernel, args):
    vault = kernel.get_engine("vault")
    if not vault:
        return "[!] Vault unavailable"
    return "Success"
```

### Conventions
*   **Engine Access:** NEVER import engines directly (e.g., `from src.core.vault import ...`). ALWAYS use `kernel.get_engine("name")`.
*   **Path Handling:** Use `os.path.join` or `pathlib` relative to `kernel.root_dir`.
*   **Output:** Return strings from `execute()`. Use `print()` only for debugging or streaming output if absolutely necessary.
*   **Encoding:** Ensure strict UTF-8 compliance for cross-platform emoji/banner support.

## Critical Files
*   `src/main.py`: Entry point and path anchoring.
*   `src/core/kernel.py`: Central orchestrator and boot sequence.
*   `src/core/eve_engine.py`: AI logic and Ollama integration.
*   `COMMAND_STANDARD.md`: The definitive guide for extending the shell.
*   `data/config/`: Configuration files (JSON).

## AI Integration (Eve)
*   Uses **Ollama** for local inference.
*   **Tiers:** Micro (Phi-3), Portable (Mistral), Mothership (Mistral-Nemo).
*   **Shadow Loading:** Caches models to host temp storage to protect USB hardware.
