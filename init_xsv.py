import os
import sys
from pathlib import Path

# --- CONFIGURATION ---
PROJECT_NAME = "xsv_core"

def create_file(path, content):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {path}")

def build_structure():
    print(f"Initializing {PROJECT_NAME}...")

    # 1. Create Directories
    dirs = [
        "specs",
        "src/commands",
        "src/core",
        "data/vault",
        "data/config",
        "tests"
    ]
    for d in dirs:
        (Path(".") / d).mkdir(parents=True, exist_ok=True)

    # 2. CREATE MANIFEST (The Law)
    manifest_content = (
        "# xsvCommandCenter - Project Manifest\n\n"
        "## 1. Prime Directives\n"
        "1. **Hybrid Portability:** Works on USB, SSD, or Cloud.\n"
        "2. **Native Integration:** Runs in native terminal.\n"
        "3. **Cross-Platform:** Uses pathlib and os.name checks.\n\n"
        "## 2. Module Registry\n"
        "| Module | Purpose |\n"
        "| :--- | :--- |\n"
        "| **Core** | Auth, Config |\n"
        "| **Vault** | Encrypted storage |\n"
        "| **Host** | OS Interaction |\n"
    )
    create_file("specs/00_MANIFEST.md", manifest_content)

    # 3. CREATE PLATFORM RULES
    platform_content = (
        "# Platform & Path Rules\n\n"
        "## 1. Path Handling\n"
        "- NEVER hardcode backslashes.\n"
        "- ALWAYS use pathlib.Path.\n\n"
        "## 2. Terminal Detection\n"
        "- Windows: Assume powershell/cmd.\n"
        "- Linux: Assume bash/zsh.\n"
    )
    create_file("specs/01_PLATFORM_RULES.md", platform_content)

    # 4. CREATE MAIN.PY
    main_py_content = (
        "import sys\n"
        "import os\n"
        "import platform\n\n"
        "def main():\n"
        "    system = platform.system()\n"
        "    if len(sys.argv) < 2:\n"
        "        print(f'xsvCommandCenter running on {system}')\n"
        "        print('Usage: xsv <command> [args]')\n"
        "        return\n\n"
        "    command = sys.argv[1].lower()\n"
        "    print(f'[{system}] Command received: {command}')\n\n"
        "if __name__ == '__main__':\n"
        "    main()\n"
    )
    create_file("src/main.py", main_py_content)
    create_file("src/__init__.py", "")

    # 5. CREATE WINDOWS LAUNCHER (BAT)
    # We use double backslashes to escape them for writing the file
    bat_content = "@echo off\npython \"%~dp0src\\main.py\" %*"
    create_file("xsv.bat", bat_content)

    # 6. CREATE LINUX LAUNCHER (SH)
    sh_content = (
        "#!/bin/bash\n"
        "DIR=\"$( cd \"$( dirname \"${BASH_SOURCE[0]}\" )\" && pwd )\"\n"
        "python3 \"$DIR/src/main.py\" \"$@\"\n"
    )
    create_file("xsv", sh_content)

    print("\nBuild Complete.")
    print("Run '.\\xsv.bat' to test.")

if __name__ == "__main__":
    build_structure()