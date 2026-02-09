# Platform & Path Rules

## 1. Path Handling
- NEVER hardcode backslashes.
- ALWAYS use pathlib.Path.

## 2. Terminal Detection
- Windows: Assume powershell/cmd.
- Linux: Assume bash/zsh.
