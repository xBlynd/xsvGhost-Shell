import subprocess
from typing import Any, List


class RootEngine:
    """The Mechanic: OS-level process and command execution."""

    def __init__(self, kernel: Any) -> None:
        self.kernel = kernel

    def run_subprocess(self, args: List[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(args, capture_output=True, text=True, check=False)
