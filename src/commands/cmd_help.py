from typing import Any, List

from core.kernel import GhostKernel


MANIFEST = {
    "name": "help",
    "desc": "Show available commands or detailed help.",
    "version": "0.1.0-phoenix",
    "usage": "help [command]",
    "author": "Ghost Core",
}


def run(args: List[str], ghost: GhostKernel) -> None:
    interface = ghost.get_engine("interface")
    loader = ghost.get_engine("loader")
    assert interface is not None
    assert loader is not None

    cmds = loader.list_commands()

    if not args:
        interface.print_info("Available commands:")
        for name, mod in sorted(cmds.items()):
            manifest = getattr(mod, "MANIFEST", {"desc": ""})
            print(f"  {name:10s} - {manifest.get('desc', '')}")
        return

    target = args[0]
    mod = cmds.get(target)
    if mod is None:
        interface.print_error(f"No such command: {target}")
        return

    manifest = getattr(mod, "MANIFEST", {})
    interface.render_command_help(manifest)
