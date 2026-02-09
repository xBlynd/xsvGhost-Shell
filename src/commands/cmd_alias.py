import sys, shutil, os
from pathlib import Path

def run(args):
    if not args:
        print("Usage: xsv alias [add|list|nuke] <name>")
        return
    cmd = args[0].lower()
    root = Path(__file__).parent.parent.parent
    
    if cmd == "add":
        if len(args) < 2: return
        new_name = args[1]
        src = root / "xsv.bat"
        tgt = root / f"{new_name}.bat"
        if src.exists():
            shutil.copy(src, tgt)
            print(f"✅ Alias '{new_name}' created.")
            
    elif cmd == "list":
        print("\n🔗 Aliases:")
        for f in root.glob("*.bat"):
            if f.name not in ["setup_xsv.bat", "setup_path.bat", "xsv.bat"]: print(f"  🔹 {f.stem}")
            
    elif cmd == "nuke":
        if len(args) < 2: return
        tgt = root / f"{args[1]}.bat"
        if tgt.exists(): 
            os.remove(tgt)
            print(f"🗑️ Nuked {args[1]}")
    else:
        print("Unknown alias command.")