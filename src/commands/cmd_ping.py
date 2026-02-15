"""
Command: ping
Enhanced ping with jitter/variance analysis via BlackBoxEngine.
"""

DESCRIPTION = "Ping with jitter analysis"
USAGE = "ping <host> [count]"
REQUIRED_ROLE = "GUEST"


def execute(kernel, args):
    """Execute enhanced ping."""
    parts = args.strip().split()
    if not parts:
        return "  Usage: ping <host> [count]\n  Example: ping 8.8.8.8 10"

    host = parts[0]
    count = 4
    if len(parts) > 1:
        try:
            count = int(parts[1])
        except ValueError:
            pass

    blackbox = kernel.get_engine("blackbox")
    if not blackbox:
        return "  [!] BlackBox engine not available"

    print(f"  Pinging {host} ({count} packets)...")
    result = blackbox.ping(host, count=count)

    # Format output
    iface = kernel.get_engine("interface")
    if iface:
        output = iface.format_ping_result(result)
    else:
        output = f"  {result}"

    # Log to vault if available
    vault = kernel.get_engine("vault")
    if vault and result.get("status") != "UNREACHABLE":
        vault.log(
            f"Ping {host}: avg={result.get('average_ms')}ms jitter={result.get('jitter_ms')}ms status={result.get('status')}",
            category="network"
        )

    return output
