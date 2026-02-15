"""
Command: clear
Clear the terminal screen.
"""

DESCRIPTION = "Clear the screen"
USAGE = "clear"
REQUIRED_ROLE = "GUEST"


import os


def execute(kernel, args):
    """Clear the terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')
    return None
