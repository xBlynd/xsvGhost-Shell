import os
from typing import Any, Dict


class InterfaceEngine:
    """The Face: banner, theming, I/O helpers.

    All visual appearance lives here so we can swap it without touching logic.
    """

    def __init__(self, kernel: Any) -> None:
        self.kernel = kernel

    # --------------------------------------------------
    # Output helpers
    # --------------------------------------------------
    def print_banner(self) -> None:
        os_name = self.kernel.os_type.upper()
        print("""\n  👻  xsv Ghost Shell (Phoenix)
  ---------------------------------
  Host OS : {os_name}
""".format(os_name=os_name))

    def print_info(self, msg: str) -> None:
        print(f"[+] {msg}")

    def print_error(self, msg: str) -> None:
        print(f"[!] {msg}")

    # --------------------------------------------------
    # Input helpers
    # --------------------------------------------------
    def read_command(self) -> str:
        return input("ghost> ")

    # --------------------------------------------------
    # Help rendering
    # --------------------------------------------------
    def render_command_help(self, manifest: Dict[str, Any]) -> None:
        self.print_info(f"{manifest.get('name')} - {manifest.get('desc')}")
        print(f"Usage : {manifest.get('usage')}")
        print(f"Author: {manifest.get('author')}")
