"""
Command: net
Network tools - check connectivity, interfaces, DNS.
"""

DESCRIPTION = "Network tools (check, interfaces, dns)"
USAGE = "net check | net interfaces | net dns <host>"
REQUIRED_ROLE = "GUEST"


def execute(kernel, args):
    """Network tools."""
    blackbox = kernel.get_engine("blackbox")
    if not blackbox:
        return "  [!] BlackBox engine not available"

    parts = args.strip().split()
    if not parts:
        return (
            "  Usage:\n"
            "    net check           Check internet connectivity\n"
            "    net interfaces      List network interfaces\n"
            "    net dns <hostname>  Resolve a hostname"
        )

    action = parts[0].lower()

    if action == "check":
        result = blackbox.check_internet()
        if result["connected"]:
            return f"  ✓ Internet connected via {result['via']} ({result['latency_ms']}ms)"
        return "  ✗ No internet connectivity"

    elif action in ("interfaces", "iface", "if"):
        interfaces = blackbox.get_interfaces()
        if not interfaces:
            return "  No interfaces found"
        lines = ["\n  Network Interfaces:"]
        for iface in interfaces:
            lines.append(f"    {iface.get('name', '?')}: {iface.get('ip', '?')}")
        return "\n".join(lines)

    elif action == "dns":
        if len(parts) < 2:
            return "  Usage: net dns <hostname>"
        result = blackbox.resolve_dns(parts[1])
        if result["resolved"]:
            return f"  ✓ {result['hostname']} -> {result['ip']}"
        return f"  ✗ Failed to resolve {result['hostname']}: {result.get('error', 'unknown')}"

    else:
        return f"  Unknown network action: {action}"
