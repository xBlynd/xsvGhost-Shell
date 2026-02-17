"""
Command: eve
Interact with the Eve AI engine.
Ask questions, check status, configure tiers and mothership connection.
"""

DESCRIPTION = "Talk to Eve AI"
USAGE = "eve ask <question> | eve status | eve setup | eve tier <name> | eve mothership <url>"
REQUIRED_ROLE = "GUEST"


def execute(kernel, args):
    """Execute eve command."""
    eve = kernel.get_engine("eve")
    if not eve:
        return "  [!] Eve engine not loaded"

    parts = args.strip().split(None, 1)
    if not parts:
        return _show_usage()

    action = parts[0].lower()
    rest = parts[1] if len(parts) > 1 else ""

    if action == "ask":
        if not rest:
            return "  Usage: eve ask <your question>"
        return _ask(eve, rest)

    elif action == "status":
        return _show_status(eve)

    elif action == "setup":
        return _show_setup_guide()

    elif action == "tier":
        if not rest:
            return _show_tiers(eve)
        return _set_tier(eve, rest.strip())

    elif action == "mothership":
        if not rest:
            return "  Usage: eve mothership <tailscale_ip:port>\n  Example: eve mothership 100.64.1.5:11434"
        return _set_mothership(eve, rest.strip())

    else:
        return _show_usage()


def _ask(eve, prompt):
    """Ask Eve a question."""
    result = eve.ask(prompt)

    if result.get("response"):
        response = result["response"]
        tier = result.get("tier", "?")
        model = result.get("model", "?")

        # Word wrap at 76 chars with indent
        lines = []
        for line in response.split('\n'):
            while len(line) > 76:
                # Try to break at a space
                break_at = line.rfind(' ', 0, 76)
                if break_at == -1:
                    break_at = 76
                lines.append("  " + line[:break_at])
                line = line[break_at:].lstrip()
            lines.append("  " + line)

        return f"\n  Eve [{tier}/{model}]:\n" + "\n".join(lines)

    error_msg = f"  [Eve] {result.get('error', 'Unknown error')}"
    if result.get("hint"):
        error_msg += f"\n  Hint: {result['hint']}"
    return error_msg


def _show_status(eve):
    """Show Eve status."""
    s = eve.get_status()
    local_icon = "✓" if s["ollama_local"] else "✗"
    remote_icon = "✓" if s.get("mothership_available") else "✗"

    lines = [
        "\n  ┌─ EVE AI STATUS ──────────────────────────┐",
        f"  │ Active Tier:   {s['active_tier']}",
        f"  │ Config Tier:   {s['configured_tier']}",
        f"  │ Local Ollama:  {local_icon} {s['ollama_url']}",
        f"  │ Mothership:    {remote_icon} {s.get('mothership_url') or 'not configured'}",
        f"  │ Shadow Load:   {'On' if s['shadow_loading'] else 'Off'}",
        f"  │ Conversation:  {s['conversation_length']} messages",
        f"  │ Version:       {s['version']}",
        "  └─────────────────────────────────────────┘",
    ]
    return "\n".join(lines)


def _show_tiers(eve):
    """Show available AI tiers."""
    lines = ["\n  ┌─ EVE AI TIERS ─┐"]
    for name, info in eve.TIER_CONFIGS.items():
        active = " ◄ ACTIVE" if name == eve.active_tier else ""
        lines.append(f"  │ {name:<12} {info['description']}")
        lines.append(f"  │              Model: {info['model'] or 'N/A'}  Size: {info['size_gb']}GB  ({info['use']}){active}")
        lines.append("  │")
    lines.append("  │ Set with: eve tier <name>  (or 'auto' for detection)")
    lines.append("  └──────────────────┘")
    return "\n".join(lines)


def _set_tier(eve, tier):
    """Set the active AI tier."""
    result = eve.set_tier(tier)
    if result.get("error"):
        return f"  [!] {result['error']}"
    return f"  ✓ Tier set to '{tier}'. Active tier: {result['active_tier']}"


def _set_mothership(eve, url):
    """Set the mothership URL."""
    if not url.startswith("http"):
        url = f"http://{url}"
    result = eve.set_mothership(url)
    return f"  ✓ Mothership set to {url}\n  Active tier: {result['active_tier']}"


def _show_usage():
    return (
        "  Eve AI Commands:\n"
        "    eve ask <question>          Ask Eve a question\n"
        "    eve status                  Show AI status and connectivity\n"
        "    eve tier                    Show available AI tiers\n"
        "    eve tier <name>             Set AI tier (auto/micro/portable/mothership)\n"
        "    eve mothership <url>        Set desktop Ollama URL (Tailscale IP)\n"
        "    eve setup                   Show Ollama installation guide"
    )


def _show_setup_guide():
    return """
  ╔═══════════════════════════════════════════════╗
  ║           EVE AI SETUP GUIDE                  ║
  ╠═══════════════════════════════════════════════╣
  ║                                               ║
  ║  Step 1: Install Ollama                       ║
  ║    https://ollama.ai                          ║
  ║    (Windows/Linux/Mac - one installer)        ║
  ║                                               ║
  ║  Step 2: Pull a model                         ║
  ║    ollama pull mistral        (7B, 4.1GB)     ║
  ║    ollama pull phi3           (3.8B, 2.3GB)   ║
  ║    ollama pull mistral-nemo   (12B, 7GB)      ║
  ║                                               ║
  ║  Step 3: Test it                              ║
  ║    > eve ask "Hello, are you working?"        ║
  ║                                               ║
  ╠═══════════════════════════════════════════════╣
  ║  REMOTE SETUP (Laptop -> Desktop)             ║
  ║                                               ║
  ║  1. Install Tailscale on both machines        ║
  ║     https://tailscale.com                     ║
  ║                                               ║
  ║  2. On desktop, run Ollama normally           ║
  ║     (it listens on :11434 by default)         ║
  ║                                               ║
  ║  3. On laptop Ghost Shell:                    ║
  ║     > eve mothership 100.x.y.z:11434          ║
  ║     (use your desktop's Tailscale IP)         ║
  ║                                               ║
  ║  Eve will auto-route heavy queries to desktop ║
  ╚═══════════════════════════════════════════════╝"""
