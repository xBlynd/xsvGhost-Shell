import os
from typing import List

from core.kernel import GhostKernel


MANIFEST = {
    "name": "pack",
    "desc": "Pack a directory into a markdown dump for AI review.",
    "version": "0.2.0-phoenix",
    "usage": "pack <path>",
    "author": "Ghost Core",
}


def run(args: List[str], ghost: GhostKernel) -> None:
    interface = ghost.get_engine("interface")
    vault = ghost.get_engine("vault")
    ghost_engine = ghost.get_engine("ghost")

    assert interface is not None
    assert vault is not None

    if not args:
        interface.print_error("Usage: pack <path>")
        return

    target = os.path.abspath(args[0])
    if not os.path.exists(target):
        interface.print_error(f"Path not found: {target}")
        return

    interface.print_info(f"Packing {target} ...")

    dump = [f"# Ghost Pack Dump\nRoot: {target}\n\n"]

    for root_dir, dirs, files in os.walk(target):
        dump.append(f"## {root_dir}\n")
        for name in files:
            path = os.path.join(root_dir, name)
            rel = os.path.relpath(path, target)
            dump.append(f"### {rel}\n")
            dump.append("```text")
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    dump.append(f.read())
            except Exception as exc:  # noqa: BLE001
                dump.append(f"[Error reading file: {exc}]")
            dump.append("```\n")

    content = "\n".join(dump)
    out_path = vault.save_text("loot", "ghost_pack", content)

    # Call into GhostEngine hook for future timestomping / stealth
    if ghost_engine is not None and hasattr(ghost_engine, "timestomp"):
        try:
            ghost_engine.timestomp(out_path)
        except Exception:
            pass

    interface.print_info(f"Pack saved to {out_path}")
