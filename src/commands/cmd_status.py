from typing import List

from core.kernel import GhostKernel


MANIFEST = {
    "name": "status",
    "desc": "Show Ghost Shell heartbeat and engine status.",
    "version": "0.1.0-phoenix",
    "usage": "status",
    "author": "Ghost Core",
}


def run(args: List[str], ghost: GhostKernel) -> None:  # noqa: ARG001
    interface = ghost.get_engine("interface")
    heartbeat = ghost.get_engine("heartbeat")

    assert interface is not None
    assert heartbeat is not None

    st = heartbeat.status()
    interface.print_info("Ghost Shell Status:")
    print(f"  Beats  : {st.get('beats')}")
    print(f"  OS     : {st.get('os_type')}")
    print("  Engines:")
    for name in st.get("engines", []):
        print(f"    - {name}")
