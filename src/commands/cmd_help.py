import sys
import os
import importlib
from pathlib import Path
from src.core.host_engine import HostEngine
from src.commands import cmd_launcher

# CONFIG
PROJECT_ROOT = Path(__file__).parent.parent.parent
SYSTEM_DIR = PROJECT_ROOT / "src" / "commands"
CUSTOM_DIR = PROJECT_ROOT / "src" / "commands" / "custom"
LIBRARY_DIR = PROJECT_ROOT / "library"

def get_commands(directory, prefix="cmd_"):
    """Scans a directory for .py files starting with prefix."""
    if not directory.exists(): return []
    cmds = []
    for f in directory.iterdir():
        if f.name.startswith(prefix) and f.name.endswith(".py"):
            name = f.name[len(prefix):-3] 
            cmds.append(name)
    return sorted(cmds)

def get_library_scripts():
    """Scans library for ANY executable script."""
    if not LIBRARY_DIR.exists(): return []
    scripts = []
    valid_exts = [".py", ".js", ".ps1", ".sh", ".bat", ".exe"]
    for f in LIBRARY_DIR.iterdir():
        if f.suffix in valid_exts:
            scripts.append(f.name)
    return sorted(scripts)

def extract_header_info(filepath):
    """Reads the first 10 lines of a file to find # Description or docstrings."""
    info = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for _ in range(15): # Read top 15 lines
                line = f.readline().strip()
                # Python Docstring
                if line.startswith('"""') or line.startswith("'''"):
                    info.append(line.strip('"').strip("'"))
                # Hash Comments
                elif line.startswith("#"):
                    comment = line.lstrip("#").strip()
                    if comment.lower().startswith("module:") or comment.lower().startswith("description:"):
                        info.append(comment)
    except: pass
    return info

def inspect_command(name):
    """Drills down into a specific command."""
    print(f"\n🔎 INSPECTING: '{name}'")
    print("-" * 40)

    found = False
    
    # 1. CHECK SYSTEM
    sys_path = SYSTEM_DIR / f"cmd_{name}.py"
    if sys_path.exists():
        print(f"TYPE:     💻 System Module")
        print(f"LOCATION: {sys_path}")
        print("STATUS:   Active Core Component")
        print("\n📄 HEADER INFO:")
        for line in extract_header_info(sys_path):
            print(f"  {line}")
        found = True

    # 2. CHECK CUSTOM
    custom_path = CUSTOM_DIR / f"cmd_{name}.py"
    if custom_path.exists():
        print(f"TYPE:     🛠️  Custom Tool")
        print(f"LOCATION: {custom_path}")
        print("STATUS:   User Module")
        print("\n📄 HEADER INFO:")
        for line in extract_header_info(custom_path):
            print(f"  {line}")
        found = True

    # 3. CHECK LIBRARY
    # We check if 'name' matches a file stem (e.g. 'matrix' -> 'matrix_prank.py')
    # Or if the user typed the full name 'matrix_prank.py'
    lib_files = get_library_scripts()
    for fname in lib_files:
        if fname == name or fname.startswith(name + "."):
            lib_path = LIBRARY_DIR / fname
            print(f"TYPE:     📚 Library Script")
            print(f"LOCATION: {lib_path}")
            print(f"RUN WITH: xsv {name}")
            print("\n📄 HEADER INFO:")
            for line in extract_header_info(lib_path):
                print(f"  {line}")
            found = True
            break

    if not found:
        print(f"❌ Command '{name}' not found in System, Custom, or Library.")
    else:
        print("-" * 40)
        print(f"💡 TIP: Run '{name}' (without args) to see its usage.")

def run(args):
    HostEngine.clear_screen()
    
    # --- DRILL DOWN MODE ---
    if args:
        target = args[0].lower()
        inspect_command(target)
        return

    # --- STANDARD MENU MODE ---
    print("\n👻 GHOST SHELL COMMANDS")
    print("=======================")

    # 1. SYSTEM
    sys_cmds = get_commands(SYSTEM_DIR)
    print(f"\n💻 SYSTEM ({len(sys_cmds)})")
    print("-" * 20)
    print(", ".join(sys_cmds))

    # 2. CUSTOM
    custom_cmds = get_commands(CUSTOM_DIR)
    if custom_cmds:
        print(f"\n🛠️  CUSTOM ({len(custom_cmds)})")
        print("-" * 20)
        print(", ".join(custom_cmds))

    # 3. LIBRARY
    lib_scripts = get_library_scripts()
    if lib_scripts:
        print(f"\n📚 LIBRARY ({len(lib_scripts)})")
        print("-" * 20)
        for s in lib_scripts:
            print(f"  • {s}")
            
    print("\n" + "="*23)
    print("Tip: Type 'help <command>' for details.")
    print("Tip: Type 'create command <name>' to build a new tool.")