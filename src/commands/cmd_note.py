from datetime import datetime
from typing import List

from core.kernel import GhostKernel


MANIFEST = {
    "name": "note",
    "desc": "Quick notes into data/vault/notes.",
    "version": "0.1.0-phoenix",
    "usage": "note <title> [text...]",
    "author": "Ghost Core",
}


def run(args: List[str], ghost: GhostKernel) -> None:
    interface = ghost.get_engine("interface")
    vault = ghost.get_engine("vault")

    assert interface is not None
    assert vault is not None

    if not args:
        interface.print_error("Usage: note <title> [text...]")
        return

    title = args[0]
    body = " ".join(args[1:]) if len(args) > 1 else ""

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n\n## {ts}\n\n{body}\n"
    path = vault.append_text("notes", title, entry)
    interface.print_info(f"Note saved to {path}")
