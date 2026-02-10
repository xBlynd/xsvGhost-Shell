import os
import json
import hashlib
import datetime
from pathlib import Path

# CONFIG
PROJECT_ROOT = Path(__file__).parent.parent.parent
VERSION_FILE = PROJECT_ROOT / "data" / "version.json"
SRC_DIR = PROJECT_ROOT / "src"
LIBRARY_DIR = PROJECT_ROOT / "library"

def load_version():
    """Loads version data or creates default if missing."""
    default = {
        "major": 6,
        "minor": 0,
        "patch": 0,
        "build": 0,
        "last_hash": "",
        "last_updated": str(datetime.datetime.now())
    }
    
    if not VERSION_FILE.exists():
        save_version(default)
        return default
        
    try:
        with open(VERSION_FILE, "r") as f:
            return json.load(f)
    except:
        return default

def save_version(data):
    """Saves version data to JSON."""
    # Ensure data dir exists
    VERSION_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(VERSION_FILE, "w") as f:
        json.dump(data, f, indent=4)

def calculate_project_hash():
    """
    Scans src/ and library/ to create a unique fingerprint of the codebase.
    If even one line of code changes, this hash changes.
    """
    hasher = hashlib.sha256()
    
    # Files to include in the fingerprint
    targets = [SRC_DIR, LIBRARY_DIR]
    
    file_paths = []
    for target in targets:
        if target.exists():
            for root, _, files in os.walk(target):
                for name in files:
                    if name.endswith(".py") or name.endswith(".js") or name.endswith(".ps1"):
                        file_paths.append(os.path.join(root, name))
    
    # Sort files to ensure hash is consistent
    for path in sorted(file_paths):
        try:
            with open(path, "rb") as f:
                buf = f.read()
                hasher.update(buf)
        except: pass
        
    return hasher.hexdigest()

def update_version(force_type=None):
    data = load_version()
    current_hash = calculate_project_hash()
    
    changed = current_hash != data["last_hash"]
    
    if not changed and not force_type:
        print(f"✅ No code changes detected.")
        print(f"   Current Version: {get_version_string(data)}")
        return

    # Logic: If code changed, bump BUILD. 
    # If user asked for 'minor'/'major', bump those.
    
    if force_type == "major":
        data["major"] += 1
        data["minor"] = 0
        data["patch"] = 0
        data["build"] = 0
        print("🚀 MAJOR UPDATE!")
        
    elif force_type == "minor":
        data["minor"] += 1
        data["patch"] = 0
        data["build"] = 0
        print("✨ Feature Update (Minor).")
        
    elif force_type == "patch":
        data["patch"] += 1
        print("🩹 Patch applied.")
        
    else:
        # Automatic Build Bump
        data["build"] += 1
        print("🔨 Code Change Detected. Bumping Build Number.")

    # Update Hash and Time
    data["last_hash"] = current_hash
    data["last_updated"] = str(datetime.datetime.now())
    
    save_version(data)
    print(f"📈 New Version: {get_version_string(data)}")

def get_version_string(data):
    return f"v{data['major']}.{data['minor']}.{data['patch']} (Build {data['build']})"

def run(args):
    if not args:
        print("\n🏷️  VERSION MANAGER")
        v = load_version()
        print(f"   Current: {get_version_string(v)}")
        print(f"   Updated: {v['last_updated']}")
        print("\nCommands:")
        print("  version check   -> Check for changes & auto-bump build #")
        print("  version patch   -> Force vX.X.+1")
        print("  version minor   -> Force vX.+1.0")
        print("  version major   -> Force v+1.0.0")
        return

    action = args[0].lower()
    
    if action == "check":
        update_version()
    elif action in ["patch", "minor", "major"]:
        update_version(action)
    else:
        print("❌ Unknown command.")