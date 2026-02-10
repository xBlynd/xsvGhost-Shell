# Specification: Host Bridge (02_HOST.md)

## 1. Objective
This module handles all Operating System interactions. We never use 'os.system' directly in other files.

## 2. Required Functions
- get_os_type(): Returns 'windows' or 'linux'.
- clear_screen(): Runs 'cls' (Windows) or 'clear' (Linux).
- launch(path): Opens a file or program safely.
- is_vm(): Checks if we are running inside Parrot OS or a VM.
