import sys
import os

# Ensure src is on the path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from core import kernel
from commands import cmd_shell


def main() -> None:
    print("\n🔌 Connecting to Ghost Kernel (Phoenix)...")
    ghost = kernel.initialize()
    cmd_shell.run(ghost)


if __name__ == "__main__":
    main()
