from datetime import datetime
from typing import List

from core.kernel import GhostKernel


MANIFEST = {
    "name": "journal",
    "desc": "Append to your daily journal in data/vault/journal.",
    "version": "0.1.0-phoenix",
    "usage": "journal [text...]",
    "author": "Ghost Core",
}


def run(args: List[str], ghost: GhostKernel) -> None:
    interface = ghost.get_engine("interface")
    vault = ghost.get_engine("vault")

    assert interface is not None
    assert vault is not None

    body = " ".join(args) if args else ""
    today = datetime.now().strftime("%Y-%m-%d")
    ts = datetime.now().strftime("%H:%M:%S")
    entry = f"\n\n## {ts}\n\n{body}\n"
    path = vault.append_text("journal", today, entry)
    interface.print_info(f"Journal updated: {path}")
