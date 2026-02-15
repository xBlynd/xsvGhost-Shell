"""
Command: legion
Manage the Legion distributed mesh network.
Currently a stub - architecture ready for implementation.
"""

DESCRIPTION = "Legion mesh network management"
USAGE = "legion status | legion nodes | legion register <address>"
REQUIRED_ROLE = "ADMIN"


def execute(kernel, args):
    """Manage Legion mesh."""
    legion = kernel.get_engine("legion")
    if not legion:
        return "  [!] Legion engine not loaded"

    parts = args.strip().split()
    if not parts:
        return _show_status(legion)

    action = parts[0].lower()

    if action == "status":
        return _show_status(legion)

    elif action == "nodes":
        return _list_nodes(legion, kernel)

    elif action == "register":
        if len(parts) < 2:
            return "  Usage: legion register <address> [label]"
        address = parts[1]
        label = " ".join(parts[2:]) if len(parts) > 2 else None
        node = legion.register_node(
            node_id=f"manual-{address.replace('.', '-').replace(':', '-')}",
            node_type="LEGIONNAIRE",
            address=address,
            label=label,
        )
        return f"  ✓ Node registered: {node['label']} ({address})"

    else:
        return (
            "  Usage:\n"
            "    legion status     Show Legion status\n"
            "    legion nodes      List known nodes\n"
            "    legion register   Register a new node"
        )


def _show_status(legion):
    status = legion.get_status()
    lines = [
        f"\n  ┌─ LEGION STATUS ─┐",
        f"  │ Operational: {'Yes' if status['operational'] else 'No (Stub)'}",
        f"  │ Node ID:     {status['node_id']}",
        f"  │ Node Type:   {status['node_type']}",
        f"  │ Known Nodes: {status['known_nodes']}",
        f"  │ Version:     {status['version']}",
        f"  └────────────────┘",
    ]
    if not status['operational']:
        lines.append("  Note: Legion Mode is stubbed. Architecture is ready.")
    return "\n".join(lines)


def _list_nodes(legion, kernel):
    nodes = legion.list_nodes()
    if not nodes:
        return "  No nodes registered. Use: legion register <address>"

    iface = kernel.get_engine("interface")
    if iface:
        headers = ["Node ID", "Type", "Address", "Label", "Status"]
        rows = []
        for n in nodes:
            self_tag = " (self)" if n.get("is_self") else ""
            rows.append([
                n["node_id"],
                n["node_type"],
                n.get("address", "local"),
                n.get("label", "?") + self_tag,
                n.get("status", "unknown"),
            ])
        return iface.format_table(headers, rows, title="LEGION NODES")

    lines = ["\n  Known Nodes:"]
    for n in nodes:
        lines.append(f"    {n['node_id']} [{n['node_type']}] - {n.get('address', 'local')}")
    return "\n".join(lines)
