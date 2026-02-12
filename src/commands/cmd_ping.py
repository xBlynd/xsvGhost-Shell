from typing import List

from core.kernel import GhostKernel


MANIFEST = {
    "name": "ping",
    "desc": "Network ping with jitter stats (Phoenix base).",
    "version": "0.2.0-phoenix",
    "usage": "ping <host> [count]",
    "author": "Ghost Core",
}


def run(args: List[str], ghost: GhostKernel) -> None:
    interface = ghost.get_engine("interface")
    blackbox = ghost.get_engine("blackbox")

    assert interface is not None
    assert blackbox is not None

    if not args:
        interface.print_error("Usage: ping <host> [count]")
        return

    host = args[0]
    count = int(args[1]) if len(args) > 1 and args[1].isdigit() else 10

    interface.print_info(f"Pinging {host} x{count} ...")

    stats = blackbox.ping(host, count=count)

    raw = stats.get("raw_output", "").strip()
    if raw:
        print(raw)

    samples = stats.get("samples", [])
    if not samples:
        interface.print_error("No RTT samples parsed.")
        return

    print("\n--- Ping Stats ---")
    print(f"min   : {stats.get('min'):.2f} ms")
    print(f"max   : {stats.get('max'):.2f} ms")
    print(f"avg   : {stats.get('avg'):.2f} ms")
    print(f"jitter: {stats.get('jitter'):.2f} ms")
