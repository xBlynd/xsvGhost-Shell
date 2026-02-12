import sys
import os
import shutil
import subprocess
from pathlib import Path

# CONFIG
PROJECT_ROOT = Path(__file__).parent.parent.parent
CUSTOM_DIR = PROJECT_ROOT / "src" / "commands" / "custom"
CORE_DIR = PROJECT_ROOT / "src" / "commands"

def find_file(name):
    # 1. Check Custom (Priority)
    f = CUSTOM_DIR / f"cmd_{name}.py"
    if f.exists(): return f

    # 2. Check Core
    f = CORE_DIR / f"cmd_{name}.py"
    if f.exists(): return f
    
    return None

def get_editor():
    # Priority List of Editors to look for
    editors = [
        "code",       # VS Code
        "subl",       # Sublime Text
        "notepad",    # Windows Default
        "nano",       # Linux Default
        "vi",         # Linux Fallback
        "vim"         # Linux Fallback
    ]
    
    for ed in editors:
        if shutil.which(ed):
            return ed
            
    if os.name == 'nt':
        return "notepad"
        
    return None

def run(args):
    print("\n📝 EDITOR LAUNCHER")
    print("-------------------")
    
    if not args:
        print("Usage: edit <command_name>")
        return

    target = args[0].lower()
    
    # 1. Find the file
    file_path = find_file(target)
    if not file_path:
        print(f"❌ Could not find command 'cmd_{target}.py'")
        print(f"   Checked: {CUSTOM_DIR}")
        print(f"   Checked: {CORE_DIR}")
        return

    # 2. Find an editor
    editor = get_editor()
    if not editor:
        print("❌ No text editor found (VS Code, Notepad, Nano, etc).")
        return

    print(f"📂 Opening '{target}' in {editor.upper()}...")
    
    # 3. Launch it
    try:
        if editor == "notepad":
            subprocess.run([editor, str(file_path)])
        else:
            # VS Code/Sublime/Nano might need shell=True depending on OS
            subprocess.call([editor, str(file_path)], shell=True)
            
        # --- YOUR CUSTOM MESSAGE ---
        print("\n👀 Look around for a text editor, Blynd.")
        print("   (Don't forget to 'reload' the command after you save!)")
        
    except Exception as e:
        print(f"❌ Failed to launch editor: {e}")