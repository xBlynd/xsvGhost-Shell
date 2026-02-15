"""
Command: status
System health dashboard showing engine status, memory, uptime.
"""

DESCRIPTION = "Show system health status"
USAGE = "status"
REQUIRED_ROLE = "GUEST"


def execute(kernel, args):
    """Display system status."""
    lines = []

    # System info
    core = kernel.get_engine("ghost_core")
    if core:
        state = core.get_state()
        lines.append("\n  ┌─ GHOST SHELL PHOENIX ─────────────────────┐")
        lines.append(f"  │ Node:     {state['node_id']}")
        lines.append(f"  │ Type:     {state['node_type']}")
        lines.append(f"  │ OS:       {state['os']} ({state['hostname']})")
        lines.append(f"  │ Python:   {state['python']}")
        lines.append(f"  │ Portable: {'Yes' if state['portable'] else 'No'}")
        lines.append(f"  │ Version:  {kernel.VERSION}")
    else:
        lines.append("\n  ┌─ GHOST SHELL PHOENIX ─────────────────────┐")
        lines.append(f"  │ Version: {kernel.VERSION}")

    # Security
    sec = kernel.get_engine("security")
    if sec:
        lines.append(f"  │ Role:     {sec.current_role}")
        lines.append(f"  │ Auth:     {'Yes' if sec.authenticated else 'No'}")

    # Health
    heartbeat = kernel.get_engine("heartbeat")
    if heartbeat:
        health = heartbeat.check_health()
        lines.append(f"  │ Status:   {health['status']}")
        lines.append(f"  │ Uptime:   {health['uptime_seconds']}s")
        lines.append(f"  │ Threads:  {health['threads']}")
        mem = health.get("memory", {})
        if mem.get("rss_mb") != "unknown":
            lines.append(f"  │ Memory:   {mem.get('rss_mb', '?')} MB")

    # Engines
    lines.append("  │")
    lines.append("  │ Engines:")
    for name, engine in kernel.engines.items():
        if engine is not None:
            ver = getattr(engine, 'ENGINE_VERSION', '?')
            op = getattr(engine, 'OPERATIONAL', True)
            status = "✓" if op else "○ stub"
            lines.append(f"  │   {status} {name:<14} v{ver}")
        else:
            lines.append(f"  │   ✗ {name:<14} FAILED")

    # Commands
    lines.append(f"  │")
    lines.append(f"  │ Commands: {len(kernel.commands)} loaded")

    # Vault stats
    vault = kernel.get_engine("vault")
    if vault:
        stats = vault.get_stats()
        lines.append(f"  │ Journal:  {stats['journal_entries']} entries")
        lines.append(f"  │ Todos:    {stats['active_todos']} active, {stats['completed_todos']} done")

    # Legion
    legion = kernel.get_engine("legion")
    if legion:
        lstatus = legion.get_status()
        lines.append(f"  │ Legion:   {'Online' if lstatus['operational'] else 'Standby'} ({lstatus['known_nodes']} nodes)")

    lines.append("  └─────────────────────────────────────────┘")

    return "\n".join(lines)
