from typing import List

from core.kernel import GhostKernel


MANIFEST = {
    "name": "reload",
    "desc": "Reload commands or specific command without restarting.",
    "version": "0.1.0-phoenix",
    "usage": "reload [command]",
    "author": "Ghost Core",
}


def run(args: List[str], ghost: GhostKernel) -> None:
    interface = ghost.get_engine("interface")
    loader = ghost.get_engine("loader")

    assert interface is not None
    assert loader is not None

    if not args:
        interface.print_info("Reloading all commands...")
        loader.reload_all()
        interface.print_info("All commands reloaded.")
        return

    name = args[0]
    ok = loader.reload_command(name)
    if not ok:
        interface.print_error(f"No such command to reload: {name}")
    else:
        interface.print_info(f"Reloaded command: {name}")
