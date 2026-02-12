from typing import List

from core.kernel import GhostKernel


MANIFEST = {
    "name": "ping",
    "desc": "Network ping stub (Phoenix v0).",
    "version": "0.1.0-phoenix",
    "usage": "ping <host>",
    "author": "Ghost Core",
}


def run(args: List[str], ghost: GhostKernel) -> None:
    interface = ghost.get_engine("interface")
    root = ghost.get_engine("root")

    assert interface is not None
    assert root is not None

    if not args:
        interface.print_error("Usage: ping <host>")
        return

    host = args[0]
    interface.print_info(f"Pinging {host} (stub) ...")
    # Phoenix v0: just run system ping once
    cmd = ["ping", "-c", "4", host] if ghost.os_type != "windows" else ["ping", "-n", "4", host]
    res = root.run_subprocess(cmd)
    print(res.stdout or res.stderr)
