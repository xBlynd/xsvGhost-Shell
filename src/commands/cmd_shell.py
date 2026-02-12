from typing import Any

from core.kernel import GhostKernel


MANIFEST = {
    "name": "shell",
    "desc": "Interactive Ghost Shell CLI.",
    "version": "0.1.0-phoenix",
    "usage": "shell",
    "author": "Ghost Core",
}


def run(ghost: GhostKernel) -> None:
    interface = ghost.get_engine("interface")
    loader = ghost.get_engine("loader")
    security = ghost.get_engine("security")

    assert interface is not None
    assert loader is not None
    assert security is not None

    if not getattr(security, "authenticated", False):
        interface.print_error("Authentication failed. Exiting.")
        return

    interface.print_banner()

    while True:
        try:
            line = interface.read_command()
        except (EOFError, KeyboardInterrupt):
            interface.print_info("Exiting Ghost Shell.")
            break

        if not line.strip():
            continue

        parts = line.strip().split()
        cmd_name, *args = parts

        if cmd_name in {"exit", "quit"}:
            interface.print_info("Goodbye.")
            break

        cmd = loader.get_command(cmd_name)
        if cmd is None:
            interface.print_error(f"Unknown command: {cmd_name}")
            continue

        try:
            cmd.run(args, ghost)  # type: ignore[attr-defined]
        except Exception as exc:  # noqa: BLE001
            interface.print_error(f"Command error: {exc}")
