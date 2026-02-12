import sys
import shutil
import os
from pathlib import Path

def run(args):
    if not args:
        print("Usage: xsv alias [add|list|nuke] <name>")
        return

    cmd = args[0].lower()
    # Define root relative to this file (src/commands/cmd_alias.py -> root)
    root = Path(__file__).parent.parent.parent
    
    # --- ADD COMMAND ---
    if cmd == "add":
        if len(args) < 2:
            print("❌ Usage: xsv alias add <name>")
            return
        
        new_name = args[1]
        src = root / "xsv.bat"
        tgt = root / f"{new_name}.bat"
        
        if not src.exists():
            print("❌ Critical: xsv.bat source not found.")
            return

        try:
            shutil.copy(src, tgt)
            print(f"✅ Alias '{new_name}' created. You can now type: {new_name}")
        except Exception as e:
            print(f"❌ Error creating alias: {e}")

    # --- LIST COMMAND ---
    elif cmd == "list":
        print("\n🔗 Active Aliases:")
        count = 0
        # Scan folder for .bat files that are NOT the system files
        for f in root.glob("*.bat"):
            if f.name not in ["setup_xsv.bat", "setup_path.bat", "xsv.bat"]: 
                print(f"  🔹 {f.stem}")
                count += 1
        if count == 0: 
            print("  (None found)")
        print("")
            
    # --- NUKE COMMAND ---
    elif cmd == "nuke":
        if len(args) < 2: 
            print("❌ Usage: xsv alias nuke <name>")
            return
            
        tgt = root / f"{args[1]}.bat"
        
        if args[1].lower() == "xsv":
            print("❌ Cannot nuke the original xsv command!")
            return

        if tgt.exists(): 
            try:
                os.remove(tgt)
                print(f"🗑️ Nuked alias: {args[1]}")
            except Exception as e:
                print(f"❌ Error deleting file: {e}")
        else:
            print(f"❌ Alias '{args[1]}' not found.")
            
    else:
        print("Unknown alias command.")